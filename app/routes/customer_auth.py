from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User
from app.models.order import Order
from app.helpers.order_status import get_order_timeline, get_order_status_label


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
    return render_template("customer/account.html")

from app.models.order import Order


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