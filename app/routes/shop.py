import os
import uuid
from datetime import UTC, datetime

import stripe
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from flask_mail import Message
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app.extensions import db, mail
from app.models.address import Address
from app.models.category import Category
from app.models.favorite import Favorite
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment_method import PaymentMethod
from app.models.product import Product
from app.models.product_review import ProductReview

shop_bp = Blueprint("shop", __name__, url_prefix="/shop")


@shop_bp.route("/test-email")
def test_email():

    msg = Message(
        subject="اختبار البريد",
        recipients=["shamanmorey@gmail.com"],
        body="إذا وصلتك هذه الرسالة فالبريد يعمل بنجاح",
    )

    try:
        mail.send(msg)
        return "✅ تم إرسال البريد"

    except Exception:
        current_app.logger.exception("Test email failed.")
    return "❌ حدث خطأ أثناء إرسال البريد."



ALLOWED_REVIEW_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_review_image(filename):
    """
    تتحقق من أن الصورة تحمل امتدادًا مسموحًا.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_REVIEW_IMAGE_EXTENSIONS
    )


def send_tracking_email(order):

    if not order.customer_email:
        print("❌ لا يوجد بريد للعميل")
        return

    tracking_url = url_for("shop.tracking", order_id=order.id, _external=True)

    current_lang = getattr(order, "language", "ar")

    # =========================
    # ARABIC
    # =========================
    if current_lang == "ar":

        subject = f"تأكيد طلبك #{order.id} - MEDIA ART"

        body = f"""
        مرحبًا {order.customer_name or ""} 🌸

        شكرًا لاختيارك MEDIA ART.

        تم استلام طلبك بنجاح ونحن نعمل الآن على مراجعته وتجهيزه.

        ━━━━━━━━━━━━━━━━━━
        رقم الطلب:
        #{order.id}
        ━━━━━━━━━━━━━━━━━━

        يمكنك تتبع حالة طلبك مباشرة عبر الرابط التالي:

        {tracking_url}

        إذا كان لديك أي استفسار يمكنك الرد على هذا البريد أو التواصل معنا عبر واتساب.

        شكرًا لثقتك بنا 💙

        MEDIA ART
        """

    # =========================
    # ENGLISH
    # =========================
    elif current_lang == "en":

        subject = f"Your Order Confirmation #{order.id} - MEDIA ART"

        body = f"""
Hello {order.customer_name or ""},

Thank you for choosing MEDIA ART.

Your order has been received successfully and is now being reviewed and prepared.

━━━━━━━━━━━━━━━━━━
Order Number:
#{order.id}
━━━━━━━━━━━━━━━━━━

You can track your order status using the link below:

{tracking_url}

If you have any questions, feel free to reply to this email or contact us via WhatsApp.

Thank you for your trust 💙

MEDIA ART
"""

    # =========================
    # JAPANESE
    # =========================
    else:

        subject = f"ご注文確認 #{order.id} - MEDIA ART"

        body = f"""
{order.customer_name or ""} 様

MEDIA ARTをご利用いただきありがとうございます。

ご注文を正常に受け付けました。
現在、ご注文内容を確認し準備を進めております。

━━━━━━━━━━━━━━━━━━
注文番号:
#{order.id}
━━━━━━━━━━━━━━━━━━

以下のリンクから注文状況をご確認いただけます：

{tracking_url}

ご不明な点がございましたら、このメールへ返信いただくかWhatsAppよりご連絡ください。

今後ともよろしくお願いいたします 💙

MEDIA ART
"""

    msg = Message(
        subject=subject,
        recipients=[order.customer_email],
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    msg.body = body
    html = render_template(
        "emails/order_confirmation.html",
        lang=current_lang,
        subject=subject,
        order=order,
        tracking_url=tracking_url,
        year=datetime.now(UTC).year,
        title=(
            "تم استلام طلبك بنجاح"
            if current_lang == "ar"
            else (
                "Your order has been received"
                if current_lang == "en"
                else "ご注文を受け付けました"
            )
        ),
        message=(
            f"مرحبًا {order.customer_name}، شكرًا لطلبك من MEDIA ART."
            if current_lang == "ar"
            else (
                f"Hello {order.customer_name}, thank you for ordering from MEDIA ART."
                if current_lang == "en"
                else f"{order.customer_name} 様、MEDIA ARTをご利用いただきありがとうございます。"
            )
        ),
        order_label=(
            "رقم الطلب"
            if current_lang == "ar"
            else "Order Number" if current_lang == "en" else "注文番号"
        ),
        track_button=(
            "تتبع الطلب"
            if current_lang == "ar"
            else "Track Order" if current_lang == "en" else "注文を追跡"
        ),
        footer_text=(
            "إذا كان لديك أي استفسار يمكنك الرد على هذا البريد."
            if current_lang == "ar"
            else (
                "If you have any questions, feel free to reply to this email."
                if current_lang == "en"
                else "ご不明な点がございましたらこのメールへご返信ください。"
            )
        ),
    )

    msg.html = html

    print("📧 جاري إرسال الإيميل إلى:", order.customer_email)

    try:
        mail.send(msg)
        print("✅ تم إرسال الإيميل بنجاح إلى:", order.customer_email)

    except Exception:
        current_app.logger.exception("Order email sending failed.")


@shop_bp.route("/", strict_slashes=False)
def index():
    categories = (
        Category.query.filter_by(is_active=True)
        .order_by(Category.display_order.asc(), Category.id.desc())
        .all()
    )

    products = Product.query.filter_by(is_active=True).order_by(Product.id.desc()).all()

    # المنتجات المفضلة للمستخدم الحالي
    favorite_ids = []

    if current_user.is_authenticated:
        favorite_ids = [
            fav.product_id
            for fav in Favorite.query.filter_by(user_id=current_user.id).all()
        ]

    return render_template(
        "shop/index.html",
        categories=categories,
        products=products,
        active_category=None,
        favorite_ids=favorite_ids,
    )


@shop_bp.route("/category/<slug>")
def category_products(slug):
    category = Category.query.filter(
        or_(
            Category.slug == slug,
            Category.slug_ar == slug,
            Category.slug_en == slug,
            Category.slug_ja == slug,
        )
    ).first_or_404()

    categories = (
        Category.query.filter_by(is_active=True)
        .order_by(Category.display_order.asc(), Category.id.desc())
        .all()
    )

    products = (
        Product.query.filter_by(category_id=category.id, is_active=True)
        .order_by(Product.id.desc())
        .all()
    )

    favorite_ids = []

    if current_user.is_authenticated:
        favorite_ids = [
            fav.product_id
            for fav in Favorite.query.filter_by(user_id=current_user.id).all()
        ]

    return render_template(
        "shop/index.html",
        categories=categories,
        products=products,
        active_category=category,
        favorite_ids=favorite_ids,
    )


@shop_bp.route("/product/<slug>")
def product(slug):

    product = Product.query.filter(
        or_(
            Product.slug == slug,
            Product.slug_ar == slug,
            Product.slug_en == slug,
            Product.slug_ja == slug,
        ),
        Product.is_active == True,
    ).first_or_404()

    current_lang = session.get("lang", "ar")

    # التقييمات المعتمدة فقط
    approved_reviews = (
        ProductReview.query.filter_by(product_id=product.id, is_approved=True)
        .order_by(ProductReview.created_at.desc())
        .all()
    )

    # التقييمات التي تسمح الإدارة بإظهار نجومها
    visible_ratings = [
        review.rating for review in approved_reviews if review.is_rating_visible
    ]

    # حساب متوسط التقييم
    if visible_ratings:
        average_rating = round(sum(visible_ratings) / len(visible_ratings), 1)
    else:
        average_rating = 0

    ratings_count = len(visible_ratings)
    
    # =========================
    # SEO الخاص بالمنتج
    # =========================

    seo_title = product.get_meta_title(current_lang)

    seo_description = (
        product.get_meta_description(current_lang)
        or product.get_description(current_lang)
        or ""
    )

    seo_keywords = product.get_keywords(current_lang) or ""

    if product.image:
        seo_image = url_for(
            "static",
            filename="uploads/" + product.image,
            _external=True,
        )
    elif product.images:
        seo_image = url_for(
            "static",
            filename="uploads/" + product.images[0].image,
            _external=True,
        )
    else:
        seo_image = url_for(
            "static",
            filename="images/logo.png",
            _external=True,
        )

    seo_url = url_for(
        "shop.product",
        slug=product.get_slug(current_lang),
        _external=True,
    )

    return render_template(
    "shop/product.html",
    product=product,
    current_lang=current_lang,
    reviews=approved_reviews,
    average_rating=average_rating,
    ratings_count=ratings_count,

    # SEO
    seo_title=seo_title,
    seo_description=seo_description,
    seo_keywords=seo_keywords,
    seo_image=seo_image,
    seo_url=seo_url,
    seo_og_type="product",
)


@shop_bp.route("/cart")
def cart():
    cart_data = session.get("cart", [])

    if not isinstance(cart_data, list):
        cart_data = []

    cart_items = []
    total = 0

    for item in cart_data:
        product = Product.query.get(int(item["product_id"]))

        if product:
            quantity = int(item.get("quantity", 1))
            item_total = product.price * quantity
            total += item_total

            cart_items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "item_total": item_total,
                    "color": item.get("color"),
                    "size": item.get("size"),
                    "custom_text": item.get("custom_text"),
                    "custom_image": item.get("custom_image"),
                }
            )

    return render_template("shop/cart.html", cart_items=cart_items, total=total)


@shop_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """
    إضافة المنتج إلى السلة.

    السلوك:
    - الطلب العادي يعيد التوجيه إلى السلة أو الدفع.
    - طلب AJAX يعيد JSON دون تحديث الصفحة.
    """

    product = Product.query.get_or_404(product_id)

    # جلب السلة الحالية
    cart = session.get("cart", [])

    # حماية في حال كانت قيمة السلة القديمة ليست قائمة
    if not isinstance(cart, list):
        cart = []

    action_type = request.form.get("action_type", "cart")

    selected_color = request.form.get("selected_color")
    selected_size = request.form.get("selected_size")
    custom_text = request.form.get("custom_text")

    item = {
        "product_id": product.id,
        "quantity": 1,
        "color": selected_color,
        "size": selected_size,
        "custom_text": custom_text,
        "custom_image": None,
    }

    # رفع الصورة المخصصة إن وجدت
    file = request.files.get("custom_image")

    if file and file.filename:
        filename = secure_filename(file.filename)

        upload_folder = os.path.join(current_app.root_path, "static", "uploads")

        os.makedirs(upload_folder, exist_ok=True)

        file.save(os.path.join(upload_folder, filename))

        item["custom_image"] = filename

    # البحث عن نفس المنتج بنفس الخيارات داخل السلة
    found = False

    for cart_item in cart:
        if (
            cart_item.get("product_id") == item["product_id"]
            and cart_item.get("color") == item["color"]
            and cart_item.get("size") == item["size"]
            and cart_item.get("custom_text") == item["custom_text"]
            and cart_item.get("custom_image") == item["custom_image"]
        ):
            cart_item["quantity"] = int(cart_item.get("quantity", 1)) + 1

            found = True
            break

    # إذا لم يكن موجودًا نضيفه كعنصر جديد
    if not found:
        cart.append(item)

    session["cart"] = cart
    session.modified = True

    # حساب إجمالي عدد القطع داخل السلة
    cart_count = 0

    for cart_item in cart:
        try:
            cart_count += int(cart_item.get("quantity", 1))
        except (TypeError, ValueError):
            cart_count += 1

    # معرفة هل الطلب جاء من JavaScript
    is_ajax_request = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    # الإضافة من بطاقة المنتج بدون تحديث الصفحة
    if is_ajax_request:
        return jsonify(
            {
                "success": True,
                "message": "تمت إضافة المنتج إلى السلة",
                "cart_count": cart_count,
                "product_id": product.id,
            }
        )

    # الطلب العادي من صفحة تفاصيل المنتج
    flash("تمت إضافة المنتج إلى السلة", "success")

    if action_type == "buy_now":
        return redirect(url_for("shop.checkout"))

    return redirect(url_for("shop.cart"))


@shop_bp.route("/product/<int:product_id>/review", methods=["POST"])
def submit_product_review(product_id):

    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()

    current_lang = session.get("lang", "ar")

    customer_name = request.form.get("customer_name", "").strip()

    customer_email = request.form.get("customer_email", "").strip()

    comment = request.form.get("comment", "").strip()

    rating_value = request.form.get("rating", "").strip()

    # التحقق من الاسم
    if not customer_name:

        if current_lang == "en":
            flash("Please enter your name.", "error")

        elif current_lang == "ja":
            flash("お名前を入力してください。", "error")

        else:
            flash("يرجى إدخال الاسم.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    # التحقق من عدد النجوم
    try:
        rating = int(rating_value)

    except (TypeError, ValueError):
        rating = 0

    if rating < 1 or rating > 5:

        if current_lang == "en":
            flash("Please select a rating from 1 to 5 stars.", "error")

        elif current_lang == "ja":
            flash("1〜5つ星の評価を選択してください。", "error")

        else:
            flash("يرجى اختيار تقييم من نجمة إلى خمس نجوم.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    # التحقق من طول البيانات
    if len(customer_name) > 120:
        flash("الاسم طويل جدًا.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    if len(customer_email) > 255:
        flash("البريد الإلكتروني طويل جدًا.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    if len(comment) > 3000:
        flash("التعليق طويل جدًا.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    review_image_filename = None
    review_image = request.files.get("review_image")

    # حفظ الصورة إن وجدت
    if review_image and review_image.filename:

        if not allowed_review_image(review_image.filename):

            if current_lang == "en":
                flash("Allowed image types: JPG, PNG and WEBP.", "error")

            elif current_lang == "ja":
                flash("使用できる画像形式はJPG、PNG、WEBPです。", "error")

            else:
                flash("أنواع الصور المسموحة: JPG وPNG وWEBP.", "error")

            return redirect(
                url_for("shop.product", slug=product.get_slug(current_lang))
            )

        original_filename = secure_filename(review_image.filename)

        extension = original_filename.rsplit(".", 1)[1].lower()

        # اسم فريد يمنع استبدال صورة بصورة أخرى
        review_image_filename = f"review_{product.id}_{uuid.uuid4().hex}.{extension}"

        review_upload_folder = os.path.join(
            current_app.root_path, "static", "uploads", "reviews"
        )

        os.makedirs(review_upload_folder, exist_ok=True)

        review_image.save(os.path.join(review_upload_folder, review_image_filename))

    review = ProductReview(
        product_id=product.id,
        customer_name=customer_name,
        customer_email=customer_email or None,
        rating=rating,
        comment=comment or None,
        image=review_image_filename,
        language=current_lang,
        is_approved=False,
        is_rating_visible=True,
        is_comment_visible=True,
        is_image_visible=True,
        ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
        user_agent=request.headers.get("User-Agent", "")[:500],
    )

    try:
        db.session.add(review)
        db.session.commit()

    except Exception:
        db.session.rollback()

        # حذف الصورة إذا فشل حفظ التقييم في قاعدة البيانات
        if review_image_filename:

            image_path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "reviews",
                review_image_filename,
            )

            if os.path.exists(image_path):
                os.remove(image_path)

        current_app.logger.exception(
            "Product review save error."
        )

        if current_lang == "en":
            flash("The review could not be submitted. Please try again.", "error")

        elif current_lang == "ja":
            flash("レビューを送信できませんでした。もう一度お試しください。", "error")

        else:
            flash("تعذر إرسال التقييم، يرجى المحاولة مرة أخرى.", "error")

        return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))

    if current_lang == "en":
        flash("Thank you. Your review will appear after approval.", "success")

    elif current_lang == "ja":
        flash("ありがとうございます。承認後にレビューが表示されます。", "success")

    else:
        flash("شكرًا لك، سيظهر تقييمك بعد مراجعته واعتماده.", "success")

    return redirect(url_for("shop.product", slug=product.get_slug(current_lang)))


@shop_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    if not isinstance(cart, list):
        cart = []

    if 0 <= product_id < len(cart):
        cart.pop(product_id)

    session["cart"] = cart
    session.modified = True

    flash("تم حذف المنتج من السلة", "success")

    return redirect(url_for("shop.cart"))


@shop_bp.route("/cart/update/<int:index>", methods=["POST"])
def update_cart(index):
    cart = session.get("cart", [])

    if not isinstance(cart, list):
        cart = []

    action = request.form.get("action")

    if 0 <= index < len(cart):
        if action == "increase":
            cart[index]["quantity"] = int(cart[index].get("quantity", 1)) + 1

        elif action == "decrease":
            cart[index]["quantity"] = int(cart[index].get("quantity", 1)) - 1

            if cart[index]["quantity"] <= 0:
                cart.pop(index)

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("shop.cart"))


@shop_bp.route("/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    session.modified = True

    flash("تم تفريغ السلة", "success")

    return redirect(url_for("shop.cart"))


@shop_bp.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart_data = session.get("cart", [])

    if not cart_data:
        flash("السلة فارغة", "error")
        return redirect(url_for("shop.cart"))

    cart_items = []
    total = 0

    addresses = []
    payment_methods = []

    if current_user.is_authenticated:

        addresses = (
            Address.query.filter_by(user_id=current_user.id)
            .order_by(Address.is_default.desc(), Address.id.desc())
            .all()
        )

        payment_methods = (
            PaymentMethod.query.filter_by(user_id=current_user.id)
            .order_by(PaymentMethod.is_default.desc(), PaymentMethod.id.desc())
            .all()
        )

    # تجهيز عناصر السلة

    for item in cart_data:

        product = Product.query.get(int(item["product_id"]))

        if not product:
            continue

        quantity = int(item.get("quantity", 1))

        item_total = product.price * quantity

        total += item_total

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
                "color": item.get("color"),
                "size": item.get("size"),
                "custom_text": item.get("custom_text"),
                "custom_image": item.get("custom_image"),
            }
        )

    if request.method == "POST":

        selected_address = None
        selected_payment = None

        payment_type = "cash"

        address_id = request.form.get("address_id")
        payment_method_id = request.form.get("payment_method_id")

        # -----------------------------
        # المستخدم المسجل
        # -----------------------------

        if current_user.is_authenticated:

            if address_id:

                selected_address = Address.query.filter_by(
                    id=address_id, user_id=current_user.id
                ).first()

            if payment_method_id in ("cash", "stripe", "paypay", "whatsapp"):

                payment_type = payment_method_id

            elif payment_method_id:

                selected_payment = PaymentMethod.query.filter_by(
                    id=int(payment_method_id), user_id=current_user.id
                ).first()

                if selected_payment:
                    payment_type = selected_payment.payment_type

            if selected_address:

                customer_name = selected_address.full_name

                customer_phone = selected_address.phone

                customer_email = current_user.email

                customer_address = (
                    f"{selected_address.prefecture} "
                    f"{selected_address.city} "
                    f"{selected_address.address_line}"
                )

            else:

                customer_name = ""
                customer_phone = ""
                customer_email = current_user.email
                customer_address = ""

        # -----------------------------
        # الضيف
        # -----------------------------

        else:

            customer_name = request.form.get("customer_name", "").strip()

            customer_phone = request.form.get("customer_phone", "").strip()

            customer_email = request.form.get("customer_email", "").strip()

            customer_address = request.form.get("customer_address", "").strip()

            if not customer_name or not customer_email:

                flash("الاسم والبريد الإلكتروني مطلوبان", "error")

                return render_template(
                    "shop/checkout.html",
                    cart_items=cart_items,
                    total=total,
                    addresses=addresses,
                    payment_methods=payment_methods,
                )

        # =====================================================
        # إنشاء الطلب
        # =====================================================

        order = Order(
            user_id=(current_user.id if current_user.is_authenticated else None),
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            customer_address=customer_address,
            language=session.get("lang", "ar"),
            total_price=total,
            status="processing",
            payment_method=payment_type,
            payment_status="unpaid",
        )

        db.session.add(order)
        db.session.flush()

        for item in cart_data:

            product = Product.query.get(int(item["product_id"]))

            if not product:
                continue

            db.session.add(
                OrderItem(
                    order_id=order.id,
                    product_title=product.get_title(session.get("lang", "ar")),
                    price=product.price,
                    quantity=int(item.get("quantity", 1)),
                    color=item.get("color"),
                    size=item.get("size"),
                    custom_text=item.get("custom_text"),
                    custom_image=item.get("custom_image"),
                )
            )

        db.session.commit()

        # =====================================================
        # التحويل حسب طريقة الدفع
        # =====================================================
        if payment_type == "cash":

            send_tracking_email(order)
            session["cart"] = []
            session.modified = True

            flash("تم إنشاء الطلب بنجاح", "success")

            return redirect(url_for("shop.order_success", order_id=order.id))

        elif payment_type in ("stripe", "card"):

            return redirect(url_for("shop.checkout_stripe", order_id=order.id))
        elif payment_type == "whatsapp":

            return redirect(url_for("shop.checkout_whatsapp", order_id=order.id))

        else:

            return redirect(url_for("shop.payment_page", order_id=order.id))

    return render_template(
        "shop/checkout.html",
        cart_items=cart_items,
        total=total,
        addresses=addresses,
        payment_methods=payment_methods,
    )

    # هنا يبدأ إنشاء الطلب


@shop_bp.route("/payment/<int:order_id>")
def payment_page(order_id):

    order = Order.query.get_or_404(order_id)

    if order.payment_method == "cash":
        return redirect(url_for("shop.order_success", order_id=order.id))

    if order.payment_method == "card":
        return redirect(url_for("shop.checkout_stripe", order_id=order.id))

    return render_template("shop/payment.html", order=order)


@shop_bp.route("/checkout/cod/<int:order_id>")
def checkout_cod(order_id):
    order = Order.query.get_or_404(order_id)

    order.payment_method = "cash"
    order.status = "processing"
    order.payment_status = "unpaid"

    db.session.commit()

    send_tracking_email(order)

    flash("تم تسجيل الطلب بنظام الدفع عند التسليم", "success")

    return redirect(url_for("shop.order_success", order_id=order.id))


@shop_bp.route("/checkout/whatsapp/<int:order_id>", methods=["POST"])
def checkout_whatsapp(order_id):
    order = Order.query.get_or_404(order_id)

    order.payment_method = "whatsapp"
    order.status = "processing"
    order.payment_status = "unpaid"

    db.session.commit()

    message = "مرحبًا، أريد طلب:%0A"

    for item in order.items:
        item_total = item.price * item.quantity
        message += (
            f"- {item.product_title} | العدد: {item.quantity} | السعر: ¥{item_total}%0A"
        )

    message += f"%0Aالإجمالي: ¥{order.total_price}%0A"
    message += f"رقم الطلب: #{order.id}"

    send_tracking_email(order)

    whatsapp_url = f"https://wa.me/817092220205?text={message}"

    return redirect(whatsapp_url)


@shop_bp.route("/checkout/stripe/<int:order_id>")
def checkout_stripe(order_id):
    flash(
        "💳 خدمة الدفع عبر Stripe قيد التجهيز وستتوفر قريبًا. يمكنك حاليًا استخدام الدفع عند الاستلام.",
        "info",
    )

    return redirect(url_for("shop.checkout"))
    order = Order.query.get_or_404(order_id)

    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]

    line_items = []

    for item in order.items:
        line_items.append(
            {
                "price_data": {
                    "currency": "jpy",
                    "product_data": {
                        "name": item.product_title,
                    },
                    "unit_amount": int(item.price),
                },
                "quantity": item.quantity,
            }
        )

    checkout_session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=url_for("shop.payment_success", order_id=order.id, _external=True),
        cancel_url=url_for("shop.checkout", _external=True),
        metadata={"order_id": str(order.id)},
    )

    order.payment_method = "stripe"
    order.payment_status = "unpaid"
    order.status = "processing"
    order.stripe_session_id = checkout_session.id

    db.session.commit()

    return redirect(checkout_session.url, code=303)


@shop_bp.route("/payment-success/<int:order_id>")
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)

    order.payment_status = "paid"
    order.status = "processing"

    db.session.commit()

    send_tracking_email(order)

    return render_template("shop/order_success.html", order=order)


@shop_bp.route("/order-success/<int:order_id>")
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("shop/order_success.html", order=order)


@shop_bp.route("/tracking", methods=["GET", "POST"])
def tracking():
    order_id = request.args.get("order_id")

    order = None
    error = None

    if order_id:
        order = Order.query.get(order_id)

        if not order:
            error = "لم يتم العثور على طلب بهذا الرقم"

    return render_template("shop/track_order.html", order=order, error=error)


@shop_bp.route("/favorite/toggle/<int:product_id>", methods=["POST"])
@login_required
def toggle_favorite(product_id):
    product = Product.query.get_or_404(product_id)

    favorite = Favorite.query.filter_by(
        user_id=current_user.id, product_id=product.id
    ).first()

    if favorite:
        db.session.delete(favorite)
        is_favorite = False
        message = "removed"
    else:
        favorite = Favorite(user_id=current_user.id, product_id=product.id)
        db.session.add(favorite)
        is_favorite = True
        message = "added"

    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {"success": True, "is_favorite": is_favorite, "message": message}

    return redirect(request.referrer or url_for("shop.index"))


@shop_bp.route("/favorites")
@login_required
def favorites():
    favorite_items = (
        Favorite.query.filter_by(user_id=current_user.id)
        .order_by(Favorite.id.desc())
        .all()
    )

    products = [
        item.product
        for item in favorite_items
        if item.product and item.product.is_active
    ]

    favorite_ids = [product.id for product in products]

    return render_template(
        "shop/favorites.html", products=products, favorite_ids=favorite_ids
    )
