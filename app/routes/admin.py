from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import os


from config import UPLOAD_FOLDER
from app.extensions import db

from app.forms.service_form import ServiceForm
from app.forms.menu_form import MenuItemForm
from app.forms.page_form import PageForm
from app.forms.home_section_form import HomeSectionForm
from app.forms.settings_form import SettingsForm
from app.forms.product_form import ProductForm
from app.forms.team_member_form import TeamMemberForm
from app.forms.category_form import CategoryForm
from app.forms.user_form import UserForm
from app.forms.project_form import ProjectForm
from app.forms.post_form import PostForm
from app.models.product_review import ProductReview


from app.models.service import Service
from app.models.menu_item import MenuItem
from app.models.page import Page
from app.models.home_section import HomeSection
from app.models.settings import SiteSetting
from flask_login import current_user
from functools import wraps
from flask_login import login_required, current_user, logout_user

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):

        if current_user.role != "admin":
            logout_user()
            flash("ليس لديك صلاحية للوصول إلى لوحة الإدارة.", "error")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view
from app.models.user import User
from werkzeug.security import generate_password_hash
from app.models.team_member import TeamMember
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.project import Project
from app.models.post import Post
from flask import send_file
from app.utils.pdf_generator import generate_invoice
from flask import render_template, request, redirect, url_for, flash
from app.models.partner import Partner
from app.models.product_image import ProductImage
from app.models.contact_message import ContactMessage
from app.models.newsletter_subscriber import NewsletterSubscriber
import csv
from io import StringIO
from flask import Response
from app.utils.image_helper import optimize_image


admin_bp = Blueprint("admin", __name__, url_prefix="/dash770813890")


@admin_bp.route("/")
@admin_required
def dashboard():
    services_count = Service.query.count()
    pages_count = Page.query.count()
    sections_count = HomeSection.query.count()
    menu_count = MenuItem.query.count()
    products_count = Product.query.count()
    orders_count = Order.query.count()
    posts_count = Post.query.count()
    projects_count = Project.query.count()

    return render_template(
        "admin/dashboard.html",
        services_count=services_count,
        pages_count=pages_count,
        sections_count=sections_count,
        menu_count=menu_count,
        products_count=products_count,
        orders_count=orders_count,
        posts_count=posts_count,
        projects_count=projects_count
    )
    
@admin_bp.route("/services")
@admin_required
def services_list():
    services = Service.query.order_by(Service.display_order.asc(), Service.id.desc()).all()
    return render_template("admin/services_list.html", services=services)



@admin_bp.route("/services/create", methods=["GET", "POST"])
@admin_required
def create_service():
    form = ServiceForm()

    if form.validate_on_submit():

        # تحقق من تكرار slug لكل لغة
        if Service.query.filter_by(slug_ar=form.slug_ar.data).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="إضافة خدمة")

        if form.slug_en.data and Service.query.filter_by(slug_en=form.slug_en.data).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="إضافة خدمة")

        if form.slug_ja.data and Service.query.filter_by(slug_ja=form.slug_ja.data).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="إضافة خدمة")
        filename = None

        if (
        form.image.data
        and hasattr(form.image.data, "filename")
        and form.image.data.filename
        ):
         filename = optimize_image(
            file=form.image.data,
            upload_folder=UPLOAD_FOLDER,
            quality=85,
            max_width=1600
        )
        
        if form.validate_on_submit():
            slug_en = form.slug_en.data.strip() if form.slug_en.data else None
            slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None
        service = Service(
            # العربية
            title_ar=form.title_ar.data,
            slug_ar=form.slug_ar.data,
            short_description_ar=form.short_description_ar.data,
            description_ar=form.description_ar.data,
            keywords_ar=form.keywords_ar.data,
            meta_title_ar=form.meta_title_ar.data,
            meta_description_ar=form.meta_description_ar.data,
            is_active_ar=form.is_active_ar.data,

            # الإنجليزية
            title_en=form.title_en.data,
            slug_en=slug_en,
            short_description_en=form.short_description_en.data,
            description_en=form.description_en.data,
            keywords_en=form.keywords_en.data,
            meta_title_en=form.meta_title_en.data,
            meta_description_en=form.meta_description_en.data,
            is_active_en=form.is_active_en.data,

            # اليابانية
            title_ja=form.title_ja.data,
            slug_ja=slug_ja,
            short_description_ja=form.short_description_ja.data,
            description_ja=form.description_ja.data,
            keywords_ja=form.keywords_ja.data,
            meta_title_ja=form.meta_title_ja.data,
            meta_description_ja=form.meta_description_ja.data,
            is_active_ja=form.is_active_ja.data,

            # عامة
            image=filename,
            icon=form.icon.data,
            booking_link=form.booking_link.data,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data
        )

        db.session.add(service)
        db.session.commit()

        flash("تمت إضافة الخدمة بنجاح", "success")
        return redirect(url_for("admin.services_list"))

    return render_template("admin/service_form.html", form=form, page_title="إضافة خدمة")

@admin_bp.route("/services/edit/<int:service_id>", methods=["GET", "POST"])
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm(obj=service)

    if form.validate_on_submit():

        # تحقق من slug لكل لغة
        if Service.query.filter(Service.slug_ar == form.slug_ar.data, Service.id != service.id).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="تعديل خدمة")

        if form.slug_en.data and Service.query.filter(Service.slug_en == form.slug_en.data, Service.id != service.id).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="تعديل خدمة")

        if form.slug_ja.data and Service.query.filter(Service.slug_ja == form.slug_ja.data, Service.id != service.id).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/service_form.html", form=form, page_title="تعديل خدمة")

        filename = service.image

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        service.image = filename

        # العربية
        service.title_ar = form.title_ar.data
        service.slug_ar = form.slug_ja.data.strip() if form.slug_ar.data else None
        service.short_description_ar = form.short_description_ar.data
        service.description_ar = form.description_ar.data
        service.keywords_ar = form.keywords_ar.data
        service.meta_title_ar = form.meta_title_ar.data
        service.meta_description_ar = form.meta_description_ar.data
        service.is_active_ar = form.is_active_ar.data

        # الإنجليزية
        service.title_en = form.title_en.data
        service.slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        service.short_description_en = form.short_description_en.data
        service.description_en = form.description_en.data
        service.keywords_en = form.keywords_en.data
        service.meta_title_en = form.meta_title_en.data
        service.meta_description_en = form.meta_description_en.data
        service.is_active_en = form.is_active_en.data

        # اليابانية
        service.title_ja = form.title_ja.data
        service.slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None
        service.short_description_ja = form.short_description_ja.data
        service.description_ja = form.description_ja.data
        service.keywords_ja = form.keywords_ja.data
        service.meta_title_ja = form.meta_title_ja.data
        service.meta_description_ja = form.meta_description_ja.data
        service.is_active_ja = form.is_active_ja.data

        # عامة
        service.icon = form.icon.data
        service.booking_link = form.booking_link.data
        service.display_order = form.display_order.data or 0
        service.is_active = form.is_active.data
        service.show_on_home = form.show_on_home.data
        
        print("=" * 50)
        print("slug_ar:", repr(form.slug_ar.data))
        print("slug_en:", repr(form.slug_en.data))
        print("slug_ja:", repr(form.slug_ja.data))
        print("=" * 50)

        db.session.commit()

        flash("تم تعديل الخدمة بنجاح", "success")
        return redirect(url_for("admin.services_list"))

    return render_template("admin/service_form.html", form=form, page_title="تعديل خدمة")

@admin_bp.route("/services/delete/<int:service_id>")
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)

    db.session.delete(service)
    db.session.commit()

    flash("تم حذف الخدمة بنجاح", "success")
    return redirect(url_for("admin.services_list"))


@admin_bp.route("/pages")
@admin_required
def pages_list():
    pages = Page.query.order_by(Page.id.desc()).all()
    return render_template("admin/pages_list.html", pages=pages)


@admin_bp.route("/pages/create", methods=["GET", "POST"])
@admin_required
def create_page():
    form = PageForm()
    form.parent_id.choices = [(0, "— لا يوجد —")] + [
    (
        p.id,
        p.title_ar or p.title
    )
    for p in Page.query
    .filter_by(is_active=True)
    .order_by(Page.display_order.asc())
    .all()
]
    if form.validate_on_submit():

        # التحقق من عدم تكرار الرابط العربي
        existing = Page.query.filter_by(
            slug_ar=form.slug_ar.data
        ).first()

        if existing:
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template(
                "admin/page_form.html",
                form=form,
                page_title="إضافة صفحة"
            )

        page = Page(
            

            # العناوين
            title=form.title_ar.data,
            title_ar=form.title_ar.data,
            title_en=form.title_en.data,
            title_ja=form.title_ja.data,

            # الروابط
            slug=form.slug_ar.data,
            slug_ar=form.slug_ar.data,
            slug_en=form.slug_en.data,
            slug_ja=form.slug_ja.data,

            # المحتوى القديم — نُبقيه مؤقتًا حتى لا تتعطل الصفحات القديمة
            content=form.content_ar.data or "",

            # المحتوى متعدد اللغات
            content_ar=form.content_ar.data,
            content_en=form.content_en.data,
            content_ja=form.content_ja.data,
            # الإعدادات
            page_type=form.page_type.data,
            template=form.template.data,
            display_order=form.display_order.data,

            # أماكن الظهور
            show_in_menu=form.show_in_menu.data,
            show_on_home=form.show_on_home.data,
            show_in_footer=form.show_in_footer.data,

            # الحالة
            is_active=form.is_active.data,
            
            parent_id = (
            form.parent_id.data
            if form.parent_id.data != 0
            else None
            ),
        )

        db.session.add(page)
        db.session.commit()

        flash("تمت إضافة الصفحة بنجاح", "success")
        return redirect(url_for("admin.pages_list"))

    return render_template(
        "admin/page_form.html",
        form=form,
        page_title="إضافة صفحة"
    )
    
@admin_bp.route("/pages/edit/<int:page_id>", methods=["GET", "POST"])
@admin_required
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)

    form = PageForm(obj=page)

    form.parent_id.choices = [(0, "— لا يوجد —")] + [
        (p.id, p.title_ar or p.title)
        for p in Page.query.filter(
            Page.is_active == True,
            Page.id != page.id
        )
        .order_by(Page.display_order.asc()).all()
    ]

    if not form.is_submitted():
        form.parent_id.data = page.parent_id or 0

    if form.validate_on_submit():

        # العناوين
        page.title = form.title_ar.data
        page.title_ar = form.title_ar.data
        page.title_en = form.title_en.data
        page.title_ja = form.title_ja.data

        # الروابط
        page.slug = form.slug_ar.data
        page.slug_ar = form.slug_ar.data
        page.slug_en = form.slug_en.data
        page.slug_ja = form.slug_ja.data

        # المحتوى القديم — نُبقيه مرتبطًا بالمحتوى العربي مؤقتًا
        page.content = form.content_ar.data or ""

        # المحتوى متعدد اللغات
        page.content_ar = form.content_ar.data
        page.content_en = form.content_en.data
        page.content_ja = form.content_ja.data

        # الإعدادات
        page.page_type = form.page_type.data
        page.parent_id = (
            form.parent_id.data
            if form.parent_id.data != 0
            else None
        )
        page.template = form.template.data
        page.display_order = form.display_order.data

        # أماكن الظهور
        page.show_in_menu = form.show_in_menu.data
        page.show_on_home = form.show_on_home.data
        page.show_in_footer = form.show_in_footer.data

        # الحالة
        page.is_active = form.is_active.data

        db.session.commit()

        flash("تم تعديل الصفحة بنجاح", "success")
        return redirect(url_for("admin.pages_list"))

    return render_template(
        "admin/page_form.html",
        form=form,
        page_title="تعديل صفحة"
    )
    
    
@admin_bp.route("/pages/delete/<int:page_id>")
@admin_required
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)

    db.session.delete(page)
    db.session.commit()

    flash("تم حذف الصفحة", "success")
    return redirect(url_for("admin.pages_list"))


@admin_bp.route("/home-sections")
@admin_required
def home_sections_list():
    sections = HomeSection.query.order_by(HomeSection.display_order.asc()).all()
    return render_template("admin/home_sections_list.html", sections=sections)


@admin_bp.route("/home-sections/create", methods=["GET", "POST"])
@admin_required
def create_home_section():
    form = HomeSectionForm()

    if form.validate_on_submit():
        filename = None

    if (
        form.image.data
        and hasattr(form.image.data, "filename")
        and form.image.data.filename
    ):
        filename = optimize_image(
            file=form.image.data,
            upload_folder=UPLOAD_FOLDER,
            quality=85,
            max_width=1600
        )

        section = HomeSection(

            # ===== قديم للتوافق =====
            title=form.title_ar.data,
            subtitle=form.subtitle_ar.data,
            button_text=form.button_text_ar.data,

            # ===== العربية =====
            title_ar=form.title_ar.data,
            subtitle_ar=form.subtitle_ar.data,
            button_text_ar=form.button_text_ar.data,

            # ===== الإنجليزية =====
            title_en=form.title_en.data,
            subtitle_en=form.subtitle_en.data,
            button_text_en=form.button_text_en.data,

            # ===== اليابانية =====
            title_ja=form.title_ja.data,
            subtitle_ja=form.subtitle_ja.data,
            button_text_ja=form.button_text_ja.data,

            # ===== عامة =====
            button_link=form.button_link.data,
            image=filename,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data
        )

        db.session.add(section)
        db.session.commit()

        flash("تمت إضافة القسم بنجاح", "success")
        return redirect(url_for("admin.home_sections_list"))

    return render_template(
        "admin/home_section_form.html",
        form=form,
        page_title="إضافة قسم"
    )


@admin_bp.route("/home-sections/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_home_section(id):
    section = HomeSection.query.get_or_404(id)
    form = HomeSectionForm(obj=section)

    if form.validate_on_submit():

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            section.image = filename

        # ===== قديم للتوافق =====
        section.title = form.title_ar.data
        section.subtitle = form.subtitle_ar.data
        section.button_text = form.button_text_ar.data

        # ===== العربية =====
        section.title_ar = form.title_ar.data
        section.subtitle_ar = form.subtitle_ar.data
        section.button_text_ar = form.button_text_ar.data

        # ===== الإنجليزية =====
        section.title_en = form.title_en.data
        section.subtitle_en = form.subtitle_en.data
        section.button_text_en = form.button_text_en.data

        # ===== اليابانية =====
        section.title_ja = form.title_ja.data
        section.subtitle_ja = form.subtitle_ja.data
        section.button_text_ja = form.button_text_ja.data

        # ===== عامة =====
        section.button_link = form.button_link.data
        section.display_order = form.display_order.data or 0
        section.is_active = form.is_active.data

        db.session.commit()

        flash("تم تعديل القسم بنجاح", "success")
        return redirect(url_for("admin.home_sections_list"))

    return render_template(
        "admin/home_section_form.html",
        form=form,
        page_title="تعديل قسم"
    )

@admin_bp.route("/home-sections/delete/<int:id>")
@admin_required
def delete_home_section(id):
    section = HomeSection.query.get_or_404(id)

    if section.image:
        image_path = os.path.join(UPLOAD_FOLDER, section.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(section)
    db.session.commit()

    flash("تم حذف القسم والصورة بنجاح", "success")
    return redirect(url_for("admin.home_sections_list"))
@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    setting = SiteSetting.query.first()

    if not setting:
        setting = SiteSetting()
        db.session.add(setting)
        db.session.commit()

    if request.method == "POST":
        if request.files.get("logo"):
            file = request.files["logo"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            setting.logo = filename

        setting.site_name = request.form.get("site_name")
        setting.footer_text = request.form.get("footer_text")
        setting.show_partners = True if request.form.get("show_partners") else False

        db.session.commit()

        flash("تم حفظ الإعدادات", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html", setting=setting)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.role != "admin":
            flash("ليس لديك صلاحية للوصول إلى هذه الصفحة", "error")
            return redirect(url_for("admin.dashboard"))

        return f(*args, **kwargs)
    return decorated_function
@admin_bp.route("/users")
@admin_required
def users_list():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin/users_list.html", users=users)


@admin_bp.route("/users/create", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        flash("تمت إضافة المستخدم بنجاح", "success")
        return redirect(url_for("admin.users_list"))

    return render_template("admin/user_form.html", form=form, page_title="إضافة مستخدم")
@admin_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        if form.password.data:
            user.set_password(form.password.data)

        user.role = form.role.data

        db.session.commit()

        flash("تم تعديل المستخدم", "success")
        return redirect(url_for("admin.users_list"))

    return render_template("admin/user_form.html", form=form)
@admin_bp.route("/users/delete/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # 🔒 حماية الأدمن
    if user.role == "admin":
        admins_count = User.query.filter_by(role="admin").count()
        if admins_count <= 1:
            flash("لا يمكن حذف آخر مدير", "error")
            return redirect(url_for("admin.users_list"))

    db.session.delete(user)
    db.session.commit()

    flash("تم حذف المستخدم", "success")
    return redirect(url_for("admin.users_list"))
@admin_bp.route("/team")
@admin_required
def team_list():
    members = TeamMember.query.order_by(TeamMember.display_order.asc(), TeamMember.id.asc()).all()
    return render_template("admin/team_list.html", members=members)


@admin_bp.route("/team/create", methods=["GET", "POST"])
@admin_required
def create_team_member():
    form = TeamMemberForm()

    if form.validate_on_submit():
        slug_ar = form.slug_ar.data.strip()
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if TeamMember.query.filter_by(slug=slug_ar).first() or TeamMember.query.filter_by(slug_ar=slug_ar).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="إضافة عضو فريق")

        if slug_en and TeamMember.query.filter_by(slug_en=slug_en).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="إضافة عضو فريق")

        if slug_ja and TeamMember.query.filter_by(slug_ja=slug_ja).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="إضافة عضو فريق")

        filename = None

        if (
            form.image.data
            and hasattr(form.image.data, "filename")
            and form.image.data.filename
        ):
            filename = optimize_image(
                file=form.image.data,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )

        member = TeamMember(
            # العربية
            name_ar=form.name_ar.data,
            slug_ar=slug_ar,
            job_title_ar=form.job_title_ar.data,
            short_bio_ar=form.short_bio_ar.data,
            full_bio_ar=form.full_bio_ar.data,

            # الإنجليزية
            name_en=form.name_en.data,
            slug_en=slug_en,
            job_title_en=form.job_title_en.data,
            short_bio_en=form.short_bio_en.data,
            full_bio_en=form.full_bio_en.data,

            # اليابانية
            name_ja=form.name_ja.data,
            slug_ja=slug_ja,
            job_title_ja=form.job_title_ja.data,
            short_bio_ja=form.short_bio_ja.data,
            full_bio_ja=form.full_bio_ja.data,

            # للتوافق القديم
            name=form.name_ar.data,
            slug=slug_ar,
            job_title=form.job_title_ar.data,
            short_bio=form.short_bio_ar.data,
            full_bio=form.full_bio_ar.data,

            image=filename,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data
        )

        db.session.add(member)
        db.session.commit()

        flash("تمت إضافة عضو الفريق بنجاح", "success")
        return redirect(url_for("admin.team_list"))

    return render_template("admin/team_form.html", form=form, page_title="إضافة عضو فريق")


@admin_bp.route("/team/edit/<int:member_id>", methods=["GET", "POST"])
@admin_required
def edit_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)
    form = TeamMemberForm(obj=member)

    if form.validate_on_submit():
        slug_ar = form.slug_ar.data.strip()
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        existing_ar = TeamMember.query.filter(
            TeamMember.slug_ar == slug_ar,
            TeamMember.id != member.id
        ).first()

        existing_old = TeamMember.query.filter(
            TeamMember.slug == slug_ar,
            TeamMember.id != member.id
        ).first()

        if existing_ar or existing_old:
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="تعديل عضو فريق")

        if slug_en and TeamMember.query.filter(
            TeamMember.slug_en == slug_en,
            TeamMember.id != member.id
        ).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="تعديل عضو فريق")

        if slug_ja and TeamMember.query.filter(
            TeamMember.slug_ja == slug_ja,
            TeamMember.id != member.id
        ).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/team_form.html", form=form, page_title="تعديل عضو فريق")

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            member.image = filename

        # العربية
        member.name_ar = form.name_ar.data
        member.slug_ar = slug_ar
        member.job_title_ar = form.job_title_ar.data
        member.short_bio_ar = form.short_bio_ar.data
        member.full_bio_ar = form.full_bio_ar.data

        # الإنجليزية
        member.name_en = form.name_en.data
        member.slug_en = slug_en
        member.job_title_en = form.job_title_en.data
        member.short_bio_en = form.short_bio_en.data
        member.full_bio_en = form.full_bio_en.data

        # اليابانية
        member.name_ja = form.name_ja.data
        member.slug_ja = slug_ja
        member.job_title_ja = form.job_title_ja.data
        member.short_bio_ja = form.short_bio_ja.data
        member.full_bio_ja = form.full_bio_ja.data

        # للتوافق القديم
        member.name = form.name_ar.data
        member.slug = slug_ar
        member.job_title = form.job_title_ar.data
        member.short_bio = form.short_bio_ar.data
        member.full_bio = form.full_bio_ar.data

        member.display_order = form.display_order.data or 0
        member.is_active = form.is_active.data
        member.show_on_home = form.show_on_home.data

        db.session.commit()

        flash("تم تعديل عضو الفريق بنجاح", "success")
        return redirect(url_for("admin.team_list"))

    return render_template("admin/team_form.html", form=form, page_title="تعديل عضو فريق")

@admin_bp.route("/team/delete/<int:member_id>")
@admin_required
def delete_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)

    if member.image:
        image_path = os.path.join(UPLOAD_FOLDER, member.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(member)
    db.session.commit()

    flash("تم حذف عضو الفريق", "success")
    return redirect(url_for("admin.team_list"))
@admin_bp.route("/categories")
@admin_required
def categories_list():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template("admin/categories_list.html", categories=categories)


@admin_bp.route("/categories/create", methods=["GET", "POST"])
@admin_required
def create_category():
    form = CategoryForm()

    if form.validate_on_submit():
        slug_ar = form.slug_ar.data.strip()
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if Category.query.filter_by(slug_ar=slug_ar).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/category_form.html", form=form, page_title="إضافة تصنيف")

        if slug_en and Category.query.filter_by(slug_en=slug_en).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/category_form.html", form=form, page_title="إضافة تصنيف")

        if slug_ja and Category.query.filter_by(slug_ja=slug_ja).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/category_form.html", form=form, page_title="إضافة تصنيف")

        filename = None

        if (
            form.image.data
            and hasattr(form.image.data, "filename")
            and form.image.data.filename
        ):
            filename = optimize_image(
                file=form.image.data,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )
        category = Category(
            name=form.name_ar.data,
            slug=slug_ar,

            image=filename,

            name_ar=form.name_ar.data,
            slug_ar=slug_ar,
            description_ar=form.description_ar.data,
            keywords_ar=form.keywords_ar.data,
            meta_title_ar=form.meta_title_ar.data,
            meta_description_ar=form.meta_description_ar.data,

            name_en=form.name_en.data,
            slug_en=slug_en,
            description_en=form.description_en.data,
            keywords_en=form.keywords_en.data,
            meta_title_en=form.meta_title_en.data,
            meta_description_en=form.meta_description_en.data,

            name_ja=form.name_ja.data,
            slug_ja=slug_ja,
            description_ja=form.description_ja.data,
            keywords_ja=form.keywords_ja.data,
            meta_title_ja=form.meta_title_ja.data,
            meta_description_ja=form.meta_description_ja.data,

            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data,
            display_order=form.display_order.data or 0
        )

        db.session.add(category)
        db.session.commit()

        flash("تمت إضافة التصنيف بنجاح", "success")
        return redirect(url_for("admin.categories_list"))

    return render_template("admin/category_form.html", form=form, page_title="إضافة تصنيف")
@admin_bp.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        existing = Category.query.filter(
            Category.slug_ar == form.slug_ar.data,
            Category.id != category.id
        ).first()

        if existing:
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/category_form.html", form=form, page_title="تعديل تصنيف")

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            category.image = filename

        # قديم للتوافق
        category.name = form.name_ar.data
        category.slug = form.slug_ar.data

        category.name_ar = form.name_ar.data
        category.slug_ar = form.slug_ar.data
        category.description_ar = form.description_ar.data
        category.keywords_ar = form.keywords_ar.data
        category.meta_title_ar = form.meta_title_ar.data
        category.meta_description_ar = form.meta_description_ar.data

        category.name_en = form.name_en.data
        category.slug_en = form.slug_en.data
        category.description_en = form.description_en.data
        category.keywords_en = form.keywords_en.data
        category.meta_title_en = form.meta_title_en.data
        category.meta_description_en = form.meta_description_en.data

        category.name_ja = form.name_ja.data
        category.slug_ja = form.slug_ja.data
        category.description_ja = form.description_ja.data
        category.keywords_ja = form.keywords_ja.data
        category.meta_title_ja = form.meta_title_ja.data
        category.meta_description_ja = form.meta_description_ja.data

        category.is_active = form.is_active.data
        category.show_on_home = form.show_on_home.data
        category.display_order = form.display_order.data or 0

        db.session.commit()

        flash("تم تعديل التصنيف بنجاح", "success")
        return redirect(url_for("admin.categories_list"))

    return render_template("admin/category_form.html", form=form, page_title="تعديل تصنيف")

@admin_bp.route("/categories/delete/<int:category_id>")
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    flash("تم حذف التصنيف بنجاح", "success")
    return redirect(url_for("admin.categories_list"))
@admin_bp.route("/products")
@admin_required
def products_list():
    """
    عرض قائمة المنتجات والتصنيفات المستخدمة في الإجراءات الجماعية.
    """

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    categories = Category.query.order_by(
        Category.display_order.asc(),
        Category.id.asc()
    ).all()

    return render_template(
        "admin/products_list.html",
        products=products,
        categories=categories
    )
@admin_bp.route("/products/bulk-action", methods=["POST"])
@admin_required
def bulk_products_action():
    """
    تنفيذ إجراء واحد على مجموعة من المنتجات المحددة.
    """

    selected_ids = request.form.getlist("product_ids")
    action = request.form.get("bulk_action", "").strip()

    # التأكد من تحديد منتجات
    if not selected_ids:
        flash("يرجى تحديد منتج واحد على الأقل.", "error")
        return redirect(url_for("admin.products_list"))

    # تحويل المعرفات إلى أرقام صحيحة فقط
    product_ids = []

    for product_id in selected_ids:
        try:
            product_ids.append(int(product_id))
        except (TypeError, ValueError):
            continue

    if not product_ids:
        flash("لم يتم العثور على منتجات صالحة للتعديل.", "error")
        return redirect(url_for("admin.products_list"))

    products = Product.query.filter(
        Product.id.in_(product_ids)
    ).all()

    if not products:
        flash("لم يتم العثور على المنتجات المحددة.", "error")
        return redirect(url_for("admin.products_list"))

    # =========================
    # نشر المنتجات
    # =========================
    if action == "activate":

        for product in products:
            product.is_active = True

        message = f"تم نشر {len(products)} منتج بنجاح."

    # =========================
    # إلغاء نشر المنتجات
    # =========================
    elif action == "deactivate":

        for product in products:
            product.is_active = False

        message = f"تم إلغاء نشر {len(products)} منتج."

    # =========================
    # إظهار في الرئيسية
    # =========================
    elif action == "show_home":

        for product in products:
            product.show_on_home = True

        message = f"تم إظهار {len(products)} منتج في الصفحة الرئيسية."

    # =========================
    # إزالة من الرئيسية
    # =========================
    elif action == "hide_home":

        for product in products:
            product.show_on_home = False

        message = f"تمت إزالة {len(products)} منتج من الصفحة الرئيسية."

    # =========================
    # تفعيل تقييم النجوم
    # =========================
    elif action == "enable_ratings":

        for product in products:
            product.ratings_enabled = True

        message = f"تم تفعيل تقييم النجوم لـ {len(products)} منتج."

    # =========================
    # إيقاف تقييم النجوم
    # =========================
    elif action == "disable_ratings":

        for product in products:
            product.ratings_enabled = False

        message = f"تم إيقاف تقييم النجوم لـ {len(products)} منتج."

    # =========================
    # تفعيل التعليقات والصور
    # =========================
    elif action == "enable_comments":

        for product in products:
            product.comments_enabled = True

        message = f"تم تفعيل التعليقات والصور لـ {len(products)} منتج."

    # =========================
    # إيقاف التعليقات والصور
    # =========================
    elif action == "disable_comments":

        for product in products:
            product.comments_enabled = False

        message = f"تم إيقاف التعليقات والصور لـ {len(products)} منتج."

    # =========================
    # تغيير التصنيف
    # =========================
    elif action == "change_category":

        category_id = request.form.get("bulk_category_id", "").strip()

        if not category_id.isdigit():
            flash("يرجى اختيار التصنيف الجديد.", "error")
            return redirect(url_for("admin.products_list"))

        category = Category.query.get(int(category_id))

        if not category:
            flash("التصنيف المحدد غير موجود.", "error")
            return redirect(url_for("admin.products_list"))

        for product in products:
            product.category_id = category.id

        message = (
            f"تم نقل {len(products)} منتج إلى تصنيف "
            f"{category.name or category.name_ar}."
        )

    # =========================
    # تعيين خصم جماعي
    # =========================
    elif action == "set_discount":

        discount_value = request.form.get(
            "bulk_discount_percent",
            ""
        ).strip()

        try:
            discount_percent = float(discount_value)
        except (TypeError, ValueError):
            flash("يرجى إدخال نسبة خصم صحيحة.", "error")
            return redirect(url_for("admin.products_list"))

        if discount_percent < 0 or discount_percent > 100:
            flash("نسبة الخصم يجب أن تكون بين 0 و100.", "error")
            return redirect(url_for("admin.products_list"))

        for product in products:
            product.discount_percent = discount_percent

        message = (
            f"تم تعيين خصم {discount_percent:g}% "
            f"على {len(products)} منتج."
        )

    # =========================
    # حذف جماعي
    # =========================
    elif action == "delete":

        deleted_count = 0

        for product in products:

            # حذف الصورة الرئيسية
            if product.image:
                image_path = os.path.join(
                    UPLOAD_FOLDER,
                    product.image
                )

                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                    except OSError:
                        pass

            # حذف الصور الإضافية
            for product_image in list(product.images):
                if product_image.image:
                    additional_image_path = os.path.join(
                        UPLOAD_FOLDER,
                        product_image.image
                    )

                    if os.path.exists(additional_image_path):
                        try:
                            os.remove(additional_image_path)
                        except OSError:
                            pass

            # حذف صور التقييمات
            for review in product.reviews.all():
                if review.image:
                    review_image_path = os.path.join(
                        current_app.root_path,
                        "static",
                        "uploads",
                        "reviews",
                        review.image
                    )

                    if os.path.exists(review_image_path):
                        try:
                            os.remove(review_image_path)
                        except OSError:
                            pass

            db.session.delete(product)
            deleted_count += 1

        message = f"تم حذف {deleted_count} منتج نهائيًا."

    else:
        flash("يرجى اختيار إجراء جماعي صحيح.", "error")
        return redirect(url_for("admin.products_list"))

    try:
        db.session.commit()

    except Exception as error:
        db.session.rollback()

        current_app.logger.exception(
            "Bulk products action failed: %s",
            error
        )

        flash(
            "تعذر تنفيذ الإجراء الجماعي. يرجى المحاولة مرة أخرى.",
            "error"
        )

        return redirect(url_for("admin.products_list"))

    flash(message, "success")

    return redirect(url_for("admin.products_list"))

@admin_bp.route("/products/create", methods=["GET", "POST"])
@admin_required
def create_product():
    form = ProductForm()

    categories = Category.query.order_by(Category.name_ar.asc(), Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name_ar or c.name) for c in categories]

    if form.validate_on_submit():
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if Product.query.filter_by(slug_ar=form.slug_ar.data).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="إضافة منتج")

        if slug_en and Product.query.filter_by(slug_en=slug_en).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="إضافة منتج")

        if slug_ja and Product.query.filter_by(slug_ja=slug_ja).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="إضافة منتج")

        filename = None

        if (
            form.image.data
            and hasattr(form.image.data, "filename")
            and form.image.data.filename
        ):
            filename = optimize_image(
                file=form.image.data,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )
        product = Product(
            title=form.title_ar.data,
            slug=form.slug_ar.data,
            description=form.description_ar.data,

            title_ar=form.title_ar.data,
            slug_ar=form.slug_ar.data,
            description_ar=form.description_ar.data,
            keywords_ar=form.keywords_ar.data,
            meta_title_ar=form.meta_title_ar.data,
            meta_description_ar=form.meta_description_ar.data,
            is_active_ar=form.is_active_ar.data,

            title_en=form.title_en.data,
            slug_en=slug_en,
            description_en=form.description_en.data,
            keywords_en=form.keywords_en.data,
            meta_title_en=form.meta_title_en.data,
            meta_description_en=form.meta_description_en.data,
            is_active_en=form.is_active_en.data,

            title_ja=form.title_ja.data,
            slug_ja=slug_ja,
            description_ja=form.description_ja.data,
            keywords_ja=form.keywords_ja.data,
            meta_title_ja=form.meta_title_ja.data,
            meta_description_ja=form.meta_description_ja.data,
            is_active_ja=form.is_active_ja.data,

            price=float(form.price.data),
            discount_percent=float(form.discount_percent.data or 0),
            image=filename,
            category_id=form.category_id.data,
            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data,

            has_colors=form.has_colors.data,
            available_colors=form.available_colors.data,
            has_sizes=form.has_sizes.data,
            available_sizes=form.available_sizes.data,

            allow_custom_text=form.allow_custom_text.data,
            allow_custom_image=form.allow_custom_image.data,
            ratings_enabled=form.ratings_enabled.data,
            comments_enabled=form.comments_enabled.data,
        )

        db.session.add(product)
        db.session.commit()

            # حفظ الصور الإضافية بعد تحسينها
    files = request.files.getlist("images")

    for file in files:
        if file and file.filename:
            extra_filename = optimize_image(
                file=file,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )

            product_image = ProductImage(
                product_id=product.id,
                image=extra_filename
            )

            db.session.add(product_image)

        db.session.commit()

        flash("تمت إضافة المنتج بنجاح", "success")
        return redirect(url_for("admin.products_list"))

    return render_template("admin/product_form.html", form=form, page_title="إضافة منتج")


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    categories = Category.query.order_by(Category.name_ar.asc(), Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name_ar or c.name) for c in categories]

    if form.validate_on_submit():
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if Product.query.filter(Product.slug_ar == form.slug_ar.data, Product.id != product.id).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="تعديل منتج")

        if slug_en and Product.query.filter(Product.slug_en == slug_en, Product.id != product.id).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="تعديل منتج")

        if slug_ja and Product.query.filter(Product.slug_ja == slug_ja, Product.id != product.id).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/product_form.html", form=form, page_title="تعديل منتج")

        if (
        form.image.data
        and hasattr(form.image.data, "filename")
        and form.image.data.filename
    ):
         filename = optimize_image(
            file=form.image.data,
            upload_folder=UPLOAD_FOLDER,
            quality=85,
            max_width=1600
        )

        product.image = filename

        product.title = form.title_ar.data
        product.slug = form.slug_ar.data
        product.description = form.description_ar.data

        product.title_ar = form.title_ar.data
        product.slug_ar = form.slug_ar.data
        product.description_ar = form.description_ar.data
        product.keywords_ar = form.keywords_ar.data
        product.meta_title_ar = form.meta_title_ar.data
        product.meta_description_ar = form.meta_description_ar.data
        product.is_active_ar = form.is_active_ar.data

        product.title_en = form.title_en.data
        product.slug_en = slug_en
        product.description_en = form.description_en.data
        product.keywords_en = form.keywords_en.data
        product.meta_title_en = form.meta_title_en.data
        product.meta_description_en = form.meta_description_en.data
        product.is_active_en = form.is_active_en.data

        product.title_ja = form.title_ja.data
        product.slug_ja = slug_ja
        product.description_ja = form.description_ja.data
        product.keywords_ja = form.keywords_ja.data
        product.meta_title_ja = form.meta_title_ja.data
        product.meta_description_ja = form.meta_description_ja.data
        product.is_active_ja = form.is_active_ja.data

        product.price = float(form.price.data)
        product.discount_percent = float(form.discount_percent.data or 0)
        product.category_id = form.category_id.data
        product.is_active = form.is_active.data
        product.show_on_home = form.show_on_home.data
        product.display_order = form.display_order.data

        product.has_colors = form.has_colors.data
        product.available_colors = form.available_colors.data
        product.has_sizes = form.has_sizes.data
        product.available_sizes = form.available_sizes.data

        product.allow_custom_text = form.allow_custom_text.data
        product.allow_custom_image = form.allow_custom_image.data
        product.ratings_enabled = form.ratings_enabled.data
        product.comments_enabled = form.comments_enabled.data

        db.session.commit()

            # حفظ الصور الإضافية الجديدة بعد تحسينها
    files = request.files.getlist("images")

    for file in files:
        if file and file.filename:
            extra_filename = optimize_image(
                file=file,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )

            product_image = ProductImage(
                product_id=product.id,
                image=extra_filename
            )

            db.session.add(product_image)
        db.session.commit()

        flash("تم تعديل المنتج بنجاح", "success")
        return redirect(url_for("admin.products_list"))

    return render_template("admin/product_form.html", form=form, page_title="تعديل منتج")

@admin_bp.route("/products/delete/<int:product_id>")
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if product.image:
        image_path = os.path.join(UPLOAD_FOLDER, product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()

    flash("تم حذف المنتج بنجاح", "success")
    return redirect(url_for("admin.products_list"))

@admin_bp.route("/products/toggle-home/<int:product_id>")
@admin_required
def toggle_product_home(product_id):
    product = Product.query.get_or_404(product_id)

    product.show_on_home = not product.show_on_home
    db.session.commit()

    flash("تم تحديث حالة الظهور في الرئيسية", "success")
    return redirect(url_for("admin.products_list"))


@admin_bp.route("/products/toggle-active/<int:product_id>")
@admin_required
def toggle_product_active(product_id):
    product = Product.query.get_or_404(product_id)

    product.is_active = not product.is_active
    db.session.commit()

    flash("تم تحديث حالة المنتج", "success")
    return redirect(url_for("admin.products_list"))

@admin_bp.route("/products/export")
@admin_required
def export_products():
    """
    تصدير جميع المنتجات إلى ملف CSV.
    """

    products = Product.query.order_by(
        Product.id.asc()
    ).all()

    output = StringIO()

    # utf-8-sig يجعل العربية تظهر صحيحة عند فتح الملف في Excel.
    output.write("\ufeff")

    writer = csv.writer(output)

    writer.writerow([
        "id",
        "title_ar",
        "slug_ar",
        "description_ar",
        "title_en",
        "slug_en",
        "description_en",
        "title_ja",
        "slug_ja",
        "description_ja",
        "price",
        "discount_percent",
        "category_id",
        "category_name",
        "display_order",
        "is_active",
        "show_on_home",
        "ratings_enabled",
        "comments_enabled",
        "has_colors",
        "available_colors",
        "has_sizes",
        "available_sizes",
        "allow_custom_text",
        "allow_custom_image",
        "image"
    ])

    for product in products:
        category_name = ""

        if product.category:
            category_name = (
                getattr(product.category, "name", None)
                or getattr(product.category, "name_ar", None)
                or ""
            )

        writer.writerow([
            product.id,
            product.title_ar or "",
            product.slug_ar or "",
            product.description_ar or "",
            product.title_en or "",
            product.slug_en or "",
            product.description_en or "",
            product.title_ja or "",
            product.slug_ja or "",
            product.description_ja or "",
            product.price or 0,
            product.discount_percent or 0,
            product.category_id or "",
            category_name,
            product.display_order or 0,
            1 if product.is_active else 0,
            1 if product.show_on_home else 0,
            1 if product.ratings_enabled else 0,
            1 if product.comments_enabled else 0,
            1 if product.has_colors else 0,
            product.available_colors or "",
            1 if product.has_sizes else 0,
            product.available_sizes or "",
            1 if product.allow_custom_text else 0,
            1 if product.allow_custom_image else 0,
            product.image or ""
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=products.csv"
    )

    return response


@admin_bp.route("/orders")
def orders_list():
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template("admin/orders_list.html", orders=orders)
@admin_bp.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/order_detail.html", order=order)
@admin_bp.route("/orders/<int:order_id>/update", methods=["POST"])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)

    status = request.form.get("status")
    payment_status = request.form.get("payment_status")

    if status:
        order.status = status

    if payment_status:
        order.payment_status = payment_status

    db.session.commit()

    flash("تم تحديث الطلب", "success")
    return redirect(url_for("admin.order_detail", order_id=order.id))

@admin_bp.route("/projects")
@admin_required
def projects_list():
    projects = Project.query.order_by(Project.display_order.asc(), Project.id.desc()).all()
    return render_template("admin/projects_list.html", projects=projects)


@admin_bp.route("/projects/create", methods=["GET", "POST"])
@admin_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        existing = Project.query.filter_by(slug=form.slug.data).first()
        if existing:
            flash("هذا الرابط المختصر مستخدم مسبقًا", "error")
            return render_template("admin/project_form.html", form=form, page_title="إضافة مشروع")

        filename = None

        if (
            form.image.data
            and hasattr(form.image.data, "filename")
            and form.image.data.filename
        ):
            filename = optimize_image(
                file=form.image.data,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )

        project = Project(

    # ===== قديم للتوافق =====
    title=form.title_ar.data,
    slug=form.slug_ar.data,
    short_description=form.short_description_ar.data,
    description=form.description_ar.data,

    # ===== العربية =====
    title_ar=form.title_ar.data,
    slug_ar=form.slug_ar.data,
    short_description_ar=form.short_description_ar.data,
    description_ar=form.description_ar.data,
    keywords_ar=form.keywords_ar.data,
    meta_title_ar=form.meta_title_ar.data,
    meta_description_ar=form.meta_description_ar.data,

    # ===== الإنجليزية =====
    title_en=form.title_en.data,
    slug_en=form.slug_en.data,
    short_description_en=form.short_description_en.data,
    description_en=form.description_en.data,
    keywords_en=form.keywords_en.data,
    meta_title_en=form.meta_title_en.data,
    meta_description_en=form.meta_description_en.data,

    # ===== اليابانية =====
    title_ja=form.title_ja.data,
    slug_ja=form.slug_ja.data,
    short_description_ja=form.short_description_ja.data,
    description_ja=form.description_ja.data,
    keywords_ja=form.keywords_ja.data,
    meta_title_ja=form.meta_title_ja.data,
    meta_description_ja=form.meta_description_ja.data,

    # ===== عامة =====
    image=filename,

    client_name=form.client_name.data,
    project_type=form.project_type.data,

    display_order=form.display_order.data or 0,
    is_active=form.is_active.data,
    show_on_home=form.show_on_home.data
)

        db.session.add(project)
        db.session.commit()

        flash("تمت إضافة المشروع بنجاح", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", form=form, page_title="إضافة مشروع")


@admin_bp.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        existing = Project.query.filter(
            Project.slug == form.slug.data,
            Project.id != project.id
        ).first()

        if existing:
            flash("هذا الرابط المختصر مستخدم مسبقًا", "error")
            return render_template("admin/project_form.html", form=form, page_title="تعديل مشروع")

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
         file = form.image.data
         filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        project.image = filename

        # ===== قديم للتوافق =====
        project.title = form.title_ar.data
        project.slug = form.slug_ar.data
        project.short_description = form.short_description_ar.data
        project.description = form.description_ar.data

        # ===== العربية =====
        project.title_ar = form.title_ar.data
        project.slug_ar = form.slug_ar.data
        project.short_description_ar = form.short_description_ar.data
        project.description_ar = form.description_ar.data
        project.keywords_ar = form.keywords_ar.data
        project.meta_title_ar = form.meta_title_ar.data
        project.meta_description_ar = form.meta_description_ar.data

        # ===== الإنجليزية =====
        project.title_en = form.title_en.data
        project.slug_en = form.slug_en.data
        project.short_description_en = form.short_description_en.data
        project.description_en = form.description_en.data
        project.keywords_en = form.keywords_en.data
        project.meta_title_en = form.meta_title_en.data
        project.meta_description_en = form.meta_description_en.data

        # ===== اليابانية =====
        project.title_ja = form.title_ja.data
        project.slug_ja = form.slug_ja.data
        project.short_description_ja = form.short_description_ja.data
        project.description_ja = form.description_ja.data
        project.keywords_ja = form.keywords_ja.data
        project.meta_title_ja = form.meta_title_ja.data
        project.meta_description_ja = form.meta_description_ja.data

        db.session.commit()

        flash("تم تعديل المشروع بنجاح", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", form=form, page_title="تعديل مشروع")


@admin_bp.route("/projects/delete/<int:project_id>")
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    flash("تم حذف المشروع بنجاح", "success")
    return redirect(url_for("admin.projects_list"))

@admin_bp.route("/posts")
@admin_required
def posts_list():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("admin/posts_list.html", posts=posts)


@admin_bp.route("/posts/create", methods=["GET", "POST"])
@admin_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        slug_ar = form.slug_ar.data.strip()
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if Post.query.filter_by(slug_ar=slug_ar).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="إضافة مقال")

        if slug_en and Post.query.filter_by(slug_en=slug_en).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="إضافة مقال")

        if slug_ja and Post.query.filter_by(slug_ja=slug_ja).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="إضافة مقال")

        filename = None

        if (
            form.image.data
            and hasattr(form.image.data, "filename")
            and form.image.data.filename
        ):
            filename = optimize_image(
                file=form.image.data,
                upload_folder=UPLOAD_FOLDER,
                quality=85,
                max_width=1600
            )

        post = Post(
            # للتوافق القديم
            title=form.title_ar.data,
            slug=slug_ar,
            excerpt=form.excerpt_ar.data,
            content=form.content_ar.data,
            keywords=form.keywords_ar.data,
            meta_title=form.meta_title_ar.data,
            meta_description=form.meta_description_ar.data,

            # العربية
            title_ar=form.title_ar.data,
            slug_ar=slug_ar,
            excerpt_ar=form.excerpt_ar.data,
            content_ar=form.content_ar.data,
            keywords_ar=form.keywords_ar.data,
            meta_title_ar=form.meta_title_ar.data,
            meta_description_ar=form.meta_description_ar.data,

            # الإنجليزية
            title_en=form.title_en.data,
            slug_en=slug_en,
            excerpt_en=form.excerpt_en.data,
            content_en=form.content_en.data,
            keywords_en=form.keywords_en.data,
            meta_title_en=form.meta_title_en.data,
            meta_description_en=form.meta_description_en.data,

            # اليابانية
            title_ja=form.title_ja.data,
            slug_ja=slug_ja,
            excerpt_ja=form.excerpt_ja.data,
            content_ja=form.content_ja.data,
            keywords_ja=form.keywords_ja.data,
            meta_title_ja=form.meta_title_ja.data,
            meta_description_ja=form.meta_description_ja.data,

            image=filename,
            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data
        )

        db.session.add(post)
        db.session.commit()

        flash("تمت إضافة المقال بنجاح", "success")
        return redirect(url_for("admin.posts_list"))

    return render_template("admin/post_form.html", form=form, page_title="إضافة مقال")


@admin_bp.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        slug_ar = form.slug_ar.data.strip()
        slug_en = form.slug_en.data.strip() if form.slug_en.data else None
        slug_ja = form.slug_ja.data.strip() if form.slug_ja.data else None

        if Post.query.filter(Post.slug_ar == slug_ar, Post.id != post.id).first():
            flash("الرابط العربي مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="تعديل مقال")

        if slug_en and Post.query.filter(Post.slug_en == slug_en, Post.id != post.id).first():
            flash("الرابط الإنجليزي مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="تعديل مقال")

        if slug_ja and Post.query.filter(Post.slug_ja == slug_ja, Post.id != post.id).first():
            flash("الرابط الياباني مستخدم مسبقًا", "error")
            return render_template("admin/post_form.html", form=form, page_title="تعديل مقال")

        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            post.image = filename

        # للتوافق القديم
        post.title = form.title_ar.data
        post.slug = slug_ar
        post.excerpt = form.excerpt_ar.data
        post.content = form.content_ar.data
        post.keywords = form.keywords_ar.data
        post.meta_title = form.meta_title_ar.data
        post.meta_description = form.meta_description_ar.data

        # العربية
        post.title_ar = form.title_ar.data
        post.slug_ar = slug_ar
        post.excerpt_ar = form.excerpt_ar.data
        post.content_ar = form.content_ar.data
        post.keywords_ar = form.keywords_ar.data
        post.meta_title_ar = form.meta_title_ar.data
        post.meta_description_ar = form.meta_description_ar.data

        # الإنجليزية
        post.title_en = form.title_en.data
        post.slug_en = slug_en
        post.excerpt_en = form.excerpt_en.data
        post.content_en = form.content_en.data
        post.keywords_en = form.keywords_en.data
        post.meta_title_en = form.meta_title_en.data
        post.meta_description_en = form.meta_description_en.data

        # اليابانية
        post.title_ja = form.title_ja.data
        post.slug_ja = slug_ja
        post.excerpt_ja = form.excerpt_ja.data
        post.content_ja = form.content_ja.data
        post.keywords_ja = form.keywords_ja.data
        post.meta_title_ja = form.meta_title_ja.data
        post.meta_description_ja = form.meta_description_ja.data

        post.is_active = form.is_active.data
        post.show_on_home = form.show_on_home.data

        db.session.commit()

        flash("تم تعديل المقال بنجاح", "success")
        return redirect(url_for("admin.posts_list"))

    return render_template("admin/post_form.html", form=form, page_title="تعديل مقال")
@admin_bp.route("/posts/delete/<int:post_id>")
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash("تم حذف المقال بنجاح", "success")
    return redirect(url_for("admin.posts_list"))
# =========================
# MENU MANAGEMENT
# =========================

@admin_bp.route("/menu")
@admin_required
def menu_list():
    items = MenuItem.query.order_by(MenuItem.display_order.asc(), MenuItem.id.asc()).all()
    return render_template("admin/menu_list.html", items=items)


@admin_bp.route("/menu/create", methods=["GET", "POST"])
@admin_required
def create_menu_item():
    form = MenuItemForm()
    
    from app.models.page import Page

    form.page_id.choices = [(0, "-- اختر صفحة --")] + [
        (page.id, page.title_ar or page.title)
        for page in Page.query.order_by(Page.display_order.asc()).all()
    ]

    if form.validate_on_submit():
        item = MenuItem(
            # للتوافق القديم
            title=form.title_ar.data,

            # اللغات
            title_ar=form.title_ar.data,
            title_en=form.title_en.data,
            title_ja=form.title_ja.data,

            is_active_ar=form.is_active_ar.data,
            is_active_en=form.is_active_en.data,
            is_active_ja=form.is_active_ja.data,

            # الرابط
            content_type=form.content_type.data or None,
            endpoint=form.endpoint.data or None,
            custom_url=form.custom_url.data or None,
            page_id=form.page_id.data or None,

            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
            show_on_home=form.show_on_home.data
        )

        db.session.add(item)
        db.session.commit()

        flash("تمت إضافة عنصر القائمة بنجاح", "success")
        return redirect(url_for("admin.menu_list"))

    return render_template(
        "admin/menu_form.html",
        form=form,
        page_title="إضافة عنصر قائمة"
        
    )
@admin_bp.route("/menu/edit/<int:item_id>", methods=["GET", "POST"])
@admin_required
def edit_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    form = MenuItemForm(obj=item)
    
    from app.models.page import Page

    form.page_id.choices = [(0, "-- اختر صفحة --")] + [
        (page.id, page.title_ar or page.title)
        for page in Page.query.order_by(Page.display_order.asc()).all()
    ]

    if request.method == "GET":
        form.page_id.data = item.page_id or 0

    if form.validate_on_submit():
        # للتوافق القديم
        item.title = form.title_ar.data

        # اللغات
        item.title_ar = form.title_ar.data
        item.title_en = form.title_en.data
        item.title_ja = form.title_ja.data

        item.is_active_ar = form.is_active_ar.data
        item.is_active_en = form.is_active_en.data
        item.is_active_ja = form.is_active_ja.data

        # الرابط
        item.content_type = form.content_type.data or None
        item.endpoint = form.endpoint.data or None
        item.custom_url = form.custom_url.data or None
        item.page_id = form.page_id.data or None

        item.display_order = form.display_order.data or 0
        item.is_active = form.is_active.data
        item.show_on_home = form.show_on_home.data

        db.session.commit()

        flash("تم تعديل عنصر القائمة بنجاح", "success")
        return redirect(url_for("admin.menu_list"))

    return render_template("admin/menu_form.html", form=form, page_title="تعديل عنصر قائمة")


@admin_bp.route("/menu/delete/<int:item_id>")
@admin_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    flash("تم حذف عنصر القائمة بنجاح", "success")
    return redirect(url_for("admin.menu_list"))

@admin_bp.route("/posts/toggle-active/<int:post_id>")
@admin_required
def toggle_post_active(post_id):
    post = Post.query.get_or_404(post_id)

    post.is_active = not post.is_active
    db.session.commit()

    flash("تم تحديث حالة المقال", "success")
    return redirect(url_for("admin.posts_list"))

@admin_bp.route("/posts/toggle-home/<int:post_id>")
@admin_required
def toggle_post_home(post_id):
    post = Post.query.get_or_404(post_id)

    post.show_on_home = not post.show_on_home
    db.session.commit()

    flash("تم تحديث عرض المقال في الرئيسية", "success")
    return redirect(url_for("admin.posts_list"))

@admin_bp.route("/projects/toggle-active/<int:project_id>")
@admin_required
def toggle_project_active(project_id):
    project = Project.query.get_or_404(project_id)

    project.is_active = not project.is_active
    db.session.commit()

    flash("تم تحديث حالة المشروع", "success")
    return redirect(url_for("admin.projects_list"))

@admin_bp.route("/projects/toggle-home/<int:project_id>")
@admin_required
def toggle_project_home(project_id):
    project = Project.query.get_or_404(project_id)

    project.show_on_home = not project.show_on_home
    db.session.commit()

    flash("تم تحديث عرض المشروع في الرئيسية", "success")
    return redirect(url_for("admin.projects_list"))

@admin_bp.route("/services/toggle-home/<int:service_id>")
@admin_required
def toggle_service_home(service_id):
    service = Service.query.get_or_404(service_id)

    service.show_on_home = not service.show_on_home

    db.session.commit()

    return redirect(url_for("admin.services_list"))



@admin_bp.route("/menu/toggle-active/<int:item_id>")
@admin_required
def toggle_menu_active(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.is_active = not item.is_active
    db.session.commit()
    flash("تم تحديث حالة العنصر", "success")
    return redirect(url_for("admin.menu_list"))

@admin_bp.route("/menu/toggle-home/<int:item_id>")
@admin_required
def toggle_menu_home(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.show_on_home = not item.show_on_home
    db.session.commit()
    flash("تم تحديث ظهور العنصر في الرئيسية", "success")
    return redirect(url_for("admin.menu_list"))

@admin_bp.route("/orders/update/<int:order_id>", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)

    # الحالات الجديدة المسموح بها
    allowed_statuses = {
        "created",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    }

    # حالات الدفع المسموح بها
    allowed_payment_statuses = {
        "unpaid",
        "paid",
        "failed",
    }

    # تحويل الحالات القديمة إلى النظام الجديد
    old_status_mapping = {
        "pending": "created",
        "in_progress": "processing",
        "completed": "delivered",
        "cancelled": "cancelled",
    }

    new_status = request.form.get("status", "").strip()
    new_payment_status = request.form.get("payment_status", "").strip()

    # تحويل القيمة القديمة إن وصلت من صفحة قديمة
    new_status = old_status_mapping.get(new_status, new_status)

    if new_status not in allowed_statuses:
        flash("حالة الطلب المحددة غير صحيحة.", "danger")
        return redirect(url_for("admin.orders_list"))

    if new_payment_status not in allowed_payment_statuses:
        flash("حالة الدفع المحددة غير صحيحة.", "danger")
        return redirect(url_for("admin.orders_list"))

    order.status = new_status
    order.payment_status = new_payment_status

    db.session.commit()

    flash("تم تحديث حالة الطلب وحالة الدفع بنجاح.", "success")
    return redirect(url_for("admin.orders_list"))

@admin_bp.route("/orders/bulk-update", methods=["POST"])
@admin_required
def bulk_update_orders():
    """
    تحديث حالة الطلب أو حالة الدفع
    لعدة طلبات في عملية واحدة.
    """

    # استقبال أرقام جميع الطلبات المحددة
    order_ids = request.form.getlist("order_ids")

    # استقبال الإجراء، مثل:
    # status:processing
    # payment:paid
    bulk_action = request.form.get(
        "bulk_action",
        ""
    ).strip()

    # التأكد من وجود طلبات محددة
    if not order_ids:
        flash(
            "لم يتم تحديد أي طلب.",
            "danger"
        )

        return redirect(
            url_for("admin.orders_list")
        )

    # التأكد من صيغة الإجراء
    if ":" not in bulk_action:
        flash(
            "الإجراء الجماعي المحدد غير صحيح.",
            "danger"
        )

        return redirect(
            url_for("admin.orders_list")
        )

    action_type, action_value = bulk_action.split(
        ":",
        1
    )

    allowed_order_statuses = {
        "created",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    }

    allowed_payment_statuses = {
        "unpaid",
        "paid",
        "failed",
    }

    # جلب الطلبات المحددة فقط
    orders = Order.query.filter(
        Order.id.in_(order_ids)
    ).all()

    if not orders:
        flash(
            "لم يتم العثور على الطلبات المحددة.",
            "danger"
        )

        return redirect(
            url_for("admin.orders_list")
        )

    # تحديث حالة الطلب
    if action_type == "status":

        if action_value not in allowed_order_statuses:
            flash(
                "حالة الطلب المحددة غير صحيحة.",
                "danger"
            )

            return redirect(
                url_for("admin.orders_list")
            )

        for order in orders:
            order.status = action_value

    # تحديث حالة الدفع
    elif action_type == "payment":

        if action_value not in allowed_payment_statuses:
            flash(
                "حالة الدفع المحددة غير صحيحة.",
                "danger"
            )

            return redirect(
                url_for("admin.orders_list")
            )

        for order in orders:
            order.payment_status = action_value

    else:
        flash(
            "نوع الإجراء المحدد غير صحيح.",
            "danger"
        )

        return redirect(
            url_for("admin.orders_list")
        )

    db.session.commit()

    flash(
        f"تم تحديث {len(orders)} طلب بنجاح.",
        "success"
    )

    return redirect(
        url_for("admin.orders_list")
    )

@admin_bp.route("/orders/<int:order_id>")
@admin_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/order_details.html", order=order)

@admin_bp.route("/order/<int:order_id>/invoice")
def order_invoice(order_id):
    order = Order.query.get_or_404(order_id)

    pdf = generate_invoice(order)

    return send_file(
        pdf,
        as_attachment=True,
        download_name=f"invoice_{order.id}.pdf",
        mimetype="application/pdf"
    )
    
@admin_bp.route("/partners")
def partners_index():
     partners = Partner.query.order_by(
     Partner.display_order.asc(),
     Partner.id.desc()
    ).all()

     return render_template("admin/partners/index.html", partners=partners)


@admin_bp.route("/partners/add", methods=["GET", "POST"])
def partners_add():
    if request.method == "POST":
        name = request.form.get("name")
        display_order = request.form.get("display_order", 0)
        is_active = True if request.form.get("is_active") == "on" else False

        image_file = request.files.get("image")

        if not name or not image_file:
            flash("الاسم والصورة مطلوبان", "error")
            return redirect(url_for("admin.partners_add"))

        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("app", "static", "uploads", filename)
        image_file.save(upload_path)

        partner = Partner(
            name=name,
            image=filename,
            display_order=display_order,
            is_active=is_active
        )

        db.session.add(partner)
        db.session.commit()

        flash("تمت إضافة الشريك بنجاح", "success")
        return redirect(url_for("admin.partners_index"))

    return render_template("admin/partners/form.html", partner=None)


@admin_bp.route("/partners/delete/<int:id>")
def partners_delete(id):
    partner = Partner.query.get_or_404(id)

    db.session.delete(partner)
    db.session.commit()

    flash("تم حذف الشريك", "success")
    return redirect(url_for("admin.partners_index"))

@admin_bp.route("/partners")
@admin_required
def partners():
    partners = Partner.query.all()
    return render_template("admin/partners.html", partners=partners)

@admin_bp.route("/partners/add", methods=["GET", "POST"])
@admin_required
def add_partner():
    if request.method == "POST":
        name = request.form.get("name")
        file = request.files.get("image")

        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        partner = Partner(name=name, image=filename)
        db.session.add(partner)
        db.session.commit()

        return redirect(url_for("admin.partners"))

    return render_template("admin/add_partner.html")

# =========================
# CONTACT MESSAGES
# =========================

@admin_bp.route("/messages")
@admin_required
def contact_messages():
    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()

    return render_template(
        "admin/contact_messages.html",
        messages=messages
    )


@admin_bp.route("/messages/<int:message_id>")
@admin_required
def contact_message_detail(message_id):
    message = ContactMessage.query.get_or_404(message_id)

    message.is_read = True
    db.session.commit()

    return render_template(
        "admin/contact_message_detail.html",
        message=message
    )


@admin_bp.route("/messages/delete/<int:message_id>")
@admin_required
def delete_contact_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)

    db.session.delete(message)
    db.session.commit()

    flash("تم حذف الرسالة", "success")

    return redirect(url_for("admin.contact_messages"))

# =========================
# NEWSLETTER SUBSCRIBERS
# =========================

@admin_bp.route("/subscribers")
@admin_required
def subscribers_list():
    language = request.args.get("language", "")
    source = request.args.get("source", "")
    status = request.args.get("status", "")

    query = NewsletterSubscriber.query

    if language:
        query = query.filter(NewsletterSubscriber.language == language)

    if source:
        query = query.filter(NewsletterSubscriber.source == source)

    if status == "active":
        query = query.filter(NewsletterSubscriber.is_active == True)

    elif status == "inactive":
        query = query.filter(NewsletterSubscriber.is_active == False)

    subscribers = query.order_by(
        NewsletterSubscriber.subscribed_at.desc()
    ).all()

    return render_template(
        "admin/subscribers_list.html",
        subscribers=subscribers,
        language=language,
        source=source,
        status=status
    )


@admin_bp.route("/subscribers/delete/<int:subscriber_id>")
@admin_required
def delete_subscriber(subscriber_id):

    subscriber = NewsletterSubscriber.query.get_or_404(
        subscriber_id
    )

    db.session.delete(subscriber)
    db.session.commit()

    flash("تم حذف المشترك", "success")

    return redirect(url_for("admin.subscribers_list"))

@admin_bp.route("/subscribers/export")
@admin_required
def export_subscribers():
    language = request.args.get("language", "")
    source = request.args.get("source", "")
    status = request.args.get("status", "")

    query = NewsletterSubscriber.query

    if language:
        query = query.filter(NewsletterSubscriber.language == language)

    if source:
        query = query.filter(NewsletterSubscriber.source == source)

    if status == "active":
        query = query.filter(NewsletterSubscriber.is_active == True)

    elif status == "inactive":
        query = query.filter(NewsletterSubscriber.is_active == False)

    subscribers = query.order_by(
        NewsletterSubscriber.subscribed_at.desc()
    ).all()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Language",
        "Source",
        "Consent Given",
        "Consent At",
        "IP Address",
        "Status",
        "Subscribed At"
    ])

    for subscriber in subscribers:
        writer.writerow([
            subscriber.id,
            subscriber.name or "",
            subscriber.email,
            subscriber.language or "",
            subscriber.source or "",
            "Yes" if subscriber.consent_given else "No",
            subscriber.consent_at.strftime("%Y-%m-%d %H:%M") if subscriber.consent_at else "",
            subscriber.ip_address or "",
            "Active" if subscriber.is_active else "Inactive",
            subscriber.subscribed_at.strftime("%Y-%m-%d %H:%M") if subscriber.subscribed_at else ""
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=subscribers.csv"

    return response

# =========================================================
# إدارة تقييمات وتعليقات المنتجات
# =========================================================

@admin_bp.route("/product-reviews")
@admin_required
def product_reviews_list():
    """
    عرض جميع تقييمات المنتجات مع دعم البحث والفلاتر.
    """

    search = request.args.get("search", "").strip()
    rating = request.args.get("rating", "").strip()
    status = request.args.get("status", "").strip()
    image_status = request.args.get("image", "").strip()
    product_id = request.args.get("product_id", "").strip()

    query = ProductReview.query

    # البحث باسم العميل أو بريده أو التعليق
    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            db.or_(
                ProductReview.customer_name.ilike(search_pattern),
                ProductReview.customer_email.ilike(search_pattern),
                ProductReview.comment.ilike(search_pattern)
            )
        )

    # فلتر عدد النجوم
    if rating in {"1", "2", "3", "4", "5"}:
        query = query.filter(
            ProductReview.rating == int(rating)
        )

    # فلتر حالة الاعتماد
    if status == "approved":
        query = query.filter(
            ProductReview.is_approved.is_(True)
        )

    elif status == "pending":
        query = query.filter(
            ProductReview.is_approved.is_(False)
        )

    # فلتر وجود الصورة
    if image_status == "with_image":
        query = query.filter(
            ProductReview.image.isnot(None),
            ProductReview.image != ""
        )

    elif image_status == "without_image":
        query = query.filter(
            db.or_(
                ProductReview.image.is_(None),
                ProductReview.image == ""
            )
        )

    # فلتر المنتج
    if product_id.isdigit():
        query = query.filter(
            ProductReview.product_id == int(product_id)
        )

    reviews = query.order_by(
        ProductReview.created_at.desc(),
        ProductReview.id.desc()
    ).all()

    products = Product.query.order_by(
        Product.title_ar.asc(),
        Product.id.asc()
    ).all()

    return render_template(
        "admin/product_reviews_list.html",
        reviews=reviews,
        products=products,
        search=search,
        rating=rating,
        status=status,
        image_status=image_status,
        selected_product_id=product_id
    )


@admin_bp.route(
    "/product-reviews/<int:review_id>/toggle-approval",
    methods=["POST"]
)
@admin_required
def toggle_product_review_approval(review_id):
    """
    اعتماد التقييم أو إعادته إلى حالة الانتظار.
    """

    review = ProductReview.query.get_or_404(review_id)

    review.is_approved = not review.is_approved

    db.session.commit()

    if review.is_approved:
        flash("تم اعتماد التقييم بنجاح.", "success")
    else:
        flash("تم إخفاء التقييم وإعادته إلى الانتظار.", "success")

    return redirect(
        request.referrer or url_for("admin.product_reviews_list")
    )


@admin_bp.route(
    "/product-reviews/<int:review_id>/toggle-rating",
    methods=["POST"]
)
@admin_required
def toggle_product_review_rating(review_id):
    """
    إظهار أو إخفاء نجوم التقييم فقط.
    """

    review = ProductReview.query.get_or_404(review_id)

    review.is_rating_visible = not review.is_rating_visible

    db.session.commit()

    if review.is_rating_visible:
        flash("تم إظهار نجوم التقييم.", "success")
    else:
        flash("تم إخفاء نجوم التقييم.", "success")

    return redirect(
        request.referrer or url_for("admin.product_reviews_list")
    )


@admin_bp.route(
    "/product-reviews/<int:review_id>/toggle-comment",
    methods=["POST"]
)
@admin_required
def toggle_product_review_comment(review_id):
    """
    إظهار أو إخفاء نص التعليق فقط.
    """

    review = ProductReview.query.get_or_404(review_id)

    review.is_comment_visible = not review.is_comment_visible

    db.session.commit()

    if review.is_comment_visible:
        flash("تم إظهار التعليق.", "success")
    else:
        flash("تم إخفاء التعليق.", "success")

    return redirect(
        request.referrer or url_for("admin.product_reviews_list")
    )


@admin_bp.route(
    "/product-reviews/<int:review_id>/toggle-image",
    methods=["POST"]
)
@admin_required
def toggle_product_review_image(review_id):
    """
    إظهار أو إخفاء صورة التقييم فقط.
    """

    review = ProductReview.query.get_or_404(review_id)

    review.is_image_visible = not review.is_image_visible

    db.session.commit()

    if review.is_image_visible:
        flash("تم إظهار صورة التقييم.", "success")
    else:
        flash("تم إخفاء صورة التقييم.", "success")

    return redirect(
        request.referrer or url_for("admin.product_reviews_list")
    )


@admin_bp.route(
    "/product-reviews/<int:review_id>/delete",
    methods=["POST"]
)
@admin_required
def delete_product_review(review_id):
    """
    حذف التقييم وصورته المرفوعة نهائيًا.
    """

    review = ProductReview.query.get_or_404(review_id)

    image_filename = review.image

    db.session.delete(review)
    db.session.commit()

    # حذف الصورة من الخادم بعد نجاح حذف السجل
    if image_filename:
        image_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            "reviews",
            image_filename
        )

        try:
            if os.path.exists(image_path):
                os.remove(image_path)

        except OSError as error:
            current_app.logger.warning(
                "تعذر حذف صورة التقييم %s: %s",
                image_filename,
                error
            )

    flash("تم حذف التقييم نهائيًا.", "success")

    return redirect(
        request.referrer or url_for("admin.product_reviews_list")
    )