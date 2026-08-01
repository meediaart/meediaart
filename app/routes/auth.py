from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.forms.login_form import LoginForm
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/log770813890", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if (
            user
            and user.role == "admin"
            and check_password_hash(user.password_hash, form.password.data)
        ):
            login_user(user)
            flash("تم تسجيل الدخول بنجاح", "success")
            return redirect(url_for("admin.dashboard"))

        elif user and user.role != "admin":
            flash("ليس لديك صلاحية للدخول إلى لوحة الإدارة", "error")

        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج", "success")
    return redirect(url_for("auth.login"))