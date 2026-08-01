from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User
from app.models.order import Order
from app.helpers.order_status import get_order_timeline, get_order_status_label
from app.forms.profile_form import ProfileForm
from app.extensions import db
from app.forms.address_form import AddressForm
from app.models.address import Address
from app.models.favorite import Favorite
from app.models.payment_method import PaymentMethod
from app.forms.payment_method_form import PaymentMethodForm

customer_auth_bp = Blueprint("customer_auth", __name__, url_prefix="/account")


@customer_auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("customer_auth.account"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not username or not email or not password:
            flash("يرجى تعبئة جميع الحقول", "error")
            return redirect(url_for("customer_auth.register"))

        if User.query.filter_by(username=username).first():
            flash("اسم المستخدم مستخدم مسبقًا", "error")
            return redirect(url_for("customer_auth.register"))

        if User.query.filter_by(email=email).first():
            flash("البريد الإلكتروني مستخدم مسبقًا", "error")
            return redirect(url_for("customer_auth.register"))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="customer"
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("تم إنشاء الحساب بنجاح", "success")
        return redirect(url_for("customer_auth.account"))

    return render_template("customer/register.html")


@customer_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("customer_auth.account"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email, role="customer").first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("تم تسجيل الدخول بنجاح", "success")
            return redirect(url_for("customer_auth.account"))

        flash("البريد الإلكتروني أو كلمة المرور غير صحيحة", "error")

    return render_template("customer/login.html")


@customer_auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج", "success")
    return redirect(url_for("shop.index"))


@customer_auth_bp.route("/")
@login_required
def account():

    orders_count = Order.query.filter_by(
        user_id=current_user.id
    ).count()

    addresses_count = Address.query.filter_by(
        user_id=current_user.id
    ).count()

    favorites_count = Favorite.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "customer/account.html",
        orders_count=orders_count,
        addresses_count=addresses_count,
        favorites_count=favorites_count
    )
    
    
@customer_auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()

    if form.validate_on_submit():

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data

        db.session.commit()

        flash("تم تحديث البيانات بنجاح", "success")

        return redirect(url_for("customer_auth.profile"))

    if request.method == "GET":

        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone

    return render_template(
        "customer/profile.html",
        form=form
    )
    
@customer_auth_bp.route("/payment-methods")
@login_required
def payment_methods():

    methods = PaymentMethod.query.filter_by(
        user_id=current_user.id
    ).order_by(
        PaymentMethod.is_default.desc(),
        PaymentMethod.id.desc()
    ).all()

    return render_template(
        "customer/payment_methods.html",
        methods=methods
    )

@customer_auth_bp.route("/orders")
@login_required
def orders():
    customer_orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(Order.id.desc()).all()

    return render_template(
        "customer/orders.html",
        orders=customer_orders
    )
    
@customer_auth_bp.route("/orders/<int:order_id>")
@login_required
def order_details(order_id):
    order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    lang = session.get("lang", "ar")

    timeline = get_order_timeline(order, lang)
    status_label = get_order_status_label(order.status, lang)

    return render_template(
        "customer/order_details.html",
        order=order,
        timeline=timeline,
        status_label=status_label
    )
    
@customer_auth_bp.route("/addresses")
@login_required
def addresses():

        addresses = Address.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Address.is_default.desc(),
            Address.id.desc()
        ).all()

        return render_template(
            "customer/addresses.html",
            addresses=addresses
        )
        
        
@customer_auth_bp.route("/addresses/new", methods=["GET", "POST"])
@login_required
def new_address():

    form = AddressForm()

    if form.validate_on_submit():

        if form.is_default.data:
            Address.query.filter_by(
                user_id=current_user.id,
                is_default=True
            ).update(
                {"is_default": False}
            )

        address = Address(
            user_id=current_user.id,

            full_name=form.full_name.data,
            phone=form.phone.data,

            postal_code=form.postal_code.data,
            prefecture=form.prefecture.data,
            city=form.city.data,

            address_line=form.address_line.data,
            building=form.building.data,

            is_default=form.is_default.data
        )

        db.session.add(address)
        db.session.commit()

        flash("تمت إضافة العنوان بنجاح", "success")

        return redirect(
            url_for("customer_auth.addresses")
        )

    return render_template(
        "customer/address_form.html",
        form=form,
        page_title="إضافة عنوان"
    )
    
    
@customer_auth_bp.route("/addresses/<int:address_id>/edit", methods=["GET", "POST"])
@login_required
def edit_address(address_id):

    address = Address.query.filter_by(
        id=address_id,
        user_id=current_user.id
    ).first_or_404()

    form = AddressForm(obj=address)

    if form.validate_on_submit():

        if form.is_default.data:

            Address.query.filter_by(
                user_id=current_user.id,
                is_default=True
            ).update({"is_default": False})

        form.populate_obj(address)

        db.session.commit()

        flash("تم تحديث العنوان بنجاح", "success")

        return redirect(
            url_for("customer_auth.addresses")
        )

    return render_template(
        "customer/address_form.html",
        form=form,
        page_title="تعديل العنوان"
    )

@customer_auth_bp.route("/addresses/<int:address_id>/delete", methods=["POST"])
@login_required
def delete_address(address_id):

    address = Address.query.filter_by(
        id=address_id,
        user_id=current_user.id
    ).first_or_404()

    was_default = address.is_default

    db.session.delete(address)
    db.session.commit()

    if was_default:

        new_default = (
            Address.query
            .filter_by(user_id=current_user.id)
            .order_by(Address.id.asc())
            .first()
        )

        if new_default:
            new_default.is_default = True
            db.session.commit()

    flash("تم حذف العنوان بنجاح", "success")

    return redirect(url_for("customer_auth.addresses"))



@customer_auth_bp.route("/addresses/<int:address_id>/default", methods=["POST"])
@login_required
def set_default_address(address_id):

    address = Address.query.filter_by(
        id=address_id,
        user_id=current_user.id
    ).first_or_404()

    Address.query.filter_by(
        user_id=current_user.id
    ).update(
        {"is_default": False}
    )

    address.is_default = True

    db.session.commit()

    flash("تم تعيين العنوان الافتراضي", "success")

    return redirect(
        url_for("customer_auth.addresses")
    )
    
@customer_auth_bp.route("/payment-methods/new", methods=["GET", "POST"])
@login_required
def new_payment_method():

    form = PaymentMethodForm()

    if form.validate_on_submit():

        if form.is_default.data:

            PaymentMethod.query.filter_by(
                user_id=current_user.id
            ).update(
                {"is_default": False}
            )

        method = PaymentMethod(
            user_id=current_user.id,
            payment_type=form.payment_type.data,
            provider=form.provider.data,
            account_name=form.account_name.data,
            account_number=form.account_number.data,
            is_default=form.is_default.data
        )

        db.session.add(method)
        db.session.commit()

        flash("تمت إضافة طريقة الدفع بنجاح", "success")

        return redirect(
            url_for("customer_auth.payment_methods")
        )

    return render_template(
        "customer/payment_method_form.html",
        form=form
    )   
    
    
@customer_auth_bp.route(
    "/payment-methods/<int:method_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_payment_method(method_id):

    method = PaymentMethod.query.filter_by(
        id=method_id,
        user_id=current_user.id
    ).first_or_404()

    form = PaymentMethodForm(obj=method)

    if form.validate_on_submit():

        if form.is_default.data:

            PaymentMethod.query.filter_by(
                user_id=current_user.id
            ).update(
                {"is_default": False}
            )

        form.populate_obj(method)

        db.session.commit()

        flash(
            "تم تحديث طريقة الدفع",
            "success"
        )

        return redirect(
            url_for(
                "customer_auth.payment_methods"
            )
        )

    return render_template(
        "customer/payment_method_form.html",
        form=form
    )
    
@customer_auth_bp.route(
    "/payment-methods/<int:method_id>/delete",
    methods=["POST"]
)
@login_required
def delete_payment_method(method_id):

    method = PaymentMethod.query.filter_by(
        id=method_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(method)
    db.session.commit()

    flash(
        "تم حذف طريقة الدفع",
        "success"
    )

    return redirect(
        url_for(
            "customer_auth.payment_methods"
        )
    ) 
        