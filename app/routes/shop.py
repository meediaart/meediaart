from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sqlalchemy import or_
from flask_mail import Message
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

import os
import stripe

from app.extensions import db, mail
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from flask import render_template
from datetime import datetime
from app.models.favorite import Favorite



shop_bp = Blueprint("shop", __name__, url_prefix="/shop")
@shop_bp.route("/test-email")
def test_email():

    msg = Message(
        subject="اختبار البريد",
        recipients=["shamanmorey@gmail.com"],
        body="إذا وصلتك هذه الرسالة فالبريد يعمل بنجاح"
    )

    try:
        mail.send(msg)
        return "✅ تم إرسال البريد"

    except Exception as e:
        return f"❌ خطأ: {e}"


def send_tracking_email(order):

    if not order.customer_email:
        print("❌ لا يوجد بريد للعميل")
        return

    tracking_url = url_for(
        "shop.tracking",
        order_id=order.id,
        _external=True
    )

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
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    html = render_template(
    "emails/order_confirmation.html",

    lang=current_lang,

    subject=subject,

    order=order,

    tracking_url=tracking_url,

    year=datetime.utcnow().year,

    title=(
        "تم استلام طلبك بنجاح"
        if current_lang == "ar"
        else "Your order has been received"
        if current_lang == "en"
        else "ご注文を受け付けました"
    ),

    message=(
        f"مرحبًا {order.customer_name}، شكرًا لطلبك من MEDIA ART."
        if current_lang == "ar"
        else f"Hello {order.customer_name}, thank you for ordering from MEDIA ART."
        if current_lang == "en"
        else f"{order.customer_name} 様、MEDIA ARTをご利用いただきありがとうございます。"
    ),

    order_label=(
        "رقم الطلب"
        if current_lang == "ar"
        else "Order Number"
        if current_lang == "en"
        else "注文番号"
    ),

    track_button=(
        "تتبع الطلب"
        if current_lang == "ar"
        else "Track Order"
        if current_lang == "en"
        else "注文を追跡"
    ),

    footer_text=(
        "إذا كان لديك أي استفسار يمكنك الرد على هذا البريد."
        if current_lang == "ar"
        else "If you have any questions, feel free to reply to this email."
        if current_lang == "en"
        else "ご不明な点がございましたらこのメールへご返信ください。"
    )
)

    msg.html = html

    print("📧 جاري إرسال الإيميل إلى:", order.customer_email)

    try:
        mail.send(msg)
        print("✅ تم إرسال الإيميل بنجاح إلى:", order.customer_email)

    except Exception as e:
        print("❌ فشل إرسال الإيميل:")
        print(e)

@shop_bp.route("/shop")
def index():
    categories = Category.query.filter_by(is_active=True).order_by(
        Category.display_order.asc(),
        Category.id.desc()
    ).all()

    products = Product.query.filter_by(
        is_active=True
    ).order_by(Product.id.desc()).all()

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
        favorite_ids=favorite_ids
    )
@shop_bp.route("/shop/category/<slug>")
def category_products(slug):
    category = Category.query.filter(
        or_(
            Category.slug == slug,
            Category.slug_ar == slug,
            Category.slug_en == slug,
            Category.slug_ja == slug
        )
    ).first_or_404()

    categories = Category.query.filter_by(is_active=True).order_by(
        Category.display_order.asc(),
        Category.id.desc()
    ).all()

    products = Product.query.filter_by(
        category_id=category.id,
        is_active=True
    ).order_by(Product.id.desc()).all()

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
        favorite_ids=favorite_ids
    )
    
    
@shop_bp.route("/product/<slug>")
def product(slug):
    product = Product.query.filter(
        or_(
            Product.slug == slug,
            Product.slug_ar == slug,
            Product.slug_en == slug,
            Product.slug_ja == slug
        ),
        Product.is_active == True
    ).first_or_404()

    current_lang = session.get("lang", "ar")

    return render_template(
        "shop/product.html",
        product=product,
        current_lang=current_lang
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

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
                "color": item.get("color"),
                "size": item.get("size"),
                "custom_text": item.get("custom_text"),
                "custom_image": item.get("custom_image")
            })

    return render_template("shop/cart.html", cart_items=cart_items, total=total)


@shop_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    cart = session.get("cart", [])

    if not isinstance(cart, list):
        cart = []

    action_type = request.form.get("action_type", "cart")

    item = {
        "product_id": product.id,
        "quantity": 1,
        "color": request.form.get("selected_color"),
        "size": request.form.get("selected_size"),
        "custom_text": request.form.get("custom_text"),
        "custom_image": None
    }

    file = request.files.get("custom_image")

    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        file.save(os.path.join(upload_folder, filename))
        item["custom_image"] = filename

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

    if not found:
        cart.append(item)

    session["cart"] = cart
    session.modified = True

    flash("تمت إضافة المنتج إلى السلة", "success")

    # ⭐ هنا الفرق
    if action_type == "buy_now":
        return redirect(url_for("shop.checkout"))

    return redirect(url_for("shop.cart"))
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

    for item in cart_data:
        product = Product.query.get(int(item["product_id"]))

        if product:
            quantity = int(item.get("quantity", 1))
            item_total = product.price * quantity
            total += item_total

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
                "color": item.get("color"),
                "size": item.get("size"),
                "custom_text": item.get("custom_text"),
                "custom_image": item.get("custom_image")
            })

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        customer_phone = request.form.get("customer_phone", "").strip()
        customer_email = request.form.get("customer_email", "").strip()
        customer_address = request.form.get("customer_address", "").strip()

        if not customer_name or not customer_email:
            flash("الاسم والبريد الإلكتروني مطلوبان", "error")
            return render_template("shop/checkout.html", cart_items=cart_items, total=total)

        order = Order(
    user_id=current_user.id if current_user.is_authenticated else None,
    customer_name=customer_name,
    customer_phone=customer_phone,
    customer_email=customer_email,
    customer_address=customer_address,
    language=session.get("lang", "ar"),
    total_price=total,
    status="processing",
    payment_method="cod",
    payment_status="unpaid"
)

        db.session.add(order)
        db.session.flush()

        for item in cart_data:
            product = Product.query.get(int(item["product_id"]))

            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_title=product.get_title(session.get("lang", "ar")),
                    price=product.price,
                    quantity=int(item.get("quantity", 1)),
                    color=item.get("color"),
                    size=item.get("size"),
                    custom_text=item.get("custom_text"),
                    custom_image=item.get("custom_image")
                )

                db.session.add(order_item)

        db.session.commit()

        send_tracking_email(order)

        session["cart"] = []
        session.modified = True

        flash("تم إنشاء الطلب بنجاح", "success")

        return redirect(url_for("shop.payment_page", order_id=order.id))

    return render_template("shop/checkout.html", cart_items=cart_items, total=total)


@shop_bp.route("/payment/<int:order_id>")
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("shop/payment.html", order=order)


@shop_bp.route("/checkout/cod/<int:order_id>", methods=["POST"])
def checkout_cod(order_id):
    order = Order.query.get_or_404(order_id)

    order.payment_method = "cod"
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
        message += f"- {item.product_title} | العدد: {item.quantity} | السعر: ¥{item_total}%0A"

    message += f"%0Aالإجمالي: ¥{order.total_price}%0A"
    message += f"رقم الطلب: #{order.id}"

    send_tracking_email(order)

    whatsapp_url = f"https://wa.me/817092220205?text={message}"

    return redirect(whatsapp_url)


@shop_bp.route("/checkout/stripe/<int:order_id>", methods=["POST"])
def checkout_stripe(order_id):
    order = Order.query.get_or_404(order_id)

    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]

    line_items = []

    for item in order.items:
        line_items.append({
            "price_data": {
                "currency": "jpy",
                "product_data": {
                    "name": item.product_title,
                },
                "unit_amount": int(item.price),
            },
            "quantity": item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=url_for("shop.payment_success", order_id=order.id, _external=True),
        cancel_url=url_for("shop.checkout", _external=True),
        metadata={
            "order_id": str(order.id)
        }
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
        user_id=current_user.id,
        product_id=product.id
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
        return {
            "success": True,
            "is_favorite": is_favorite,
            "message": message
        }

    return redirect(request.referrer or url_for("shop.index"))
@shop_bp.route("/favorites")
@login_required
def favorites():
    favorite_items = Favorite.query.filter_by(
        user_id=current_user.id
    ).order_by(Favorite.id.desc()).all()

    products = [
        item.product
        for item in favorite_items
        if item.product and item.product.is_active
    ]

    favorite_ids = [product.id for product in products]

    return render_template(
        "shop/favorites.html",
        products=products,
        favorite_ids=favorite_ids
    )
