from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.page import Page
from app.models.service import Service
from app.models.home_section import HomeSection
from app.models.settings import SiteSetting
from app.models.team_member import TeamMember
from app.models.post import Post
from app.models.product import Product
from app.models.project import Project
main_bp = Blueprint("main", __name__)
from app.models.menu_item import MenuItem
from app.models.team_member import TeamMember
from app.models.partner import Partner
from app.models.category import Category

@main_bp.route("/set-language/<lang>")
def set_language(lang):
    session["lang"] = lang
    return redirect(request.referrer or url_for("main.home"))


@main_bp.route("/")
def home():
    current_lang = session.get("lang", "ar")

    home_menu_items = MenuItem.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(
        MenuItem.display_order.asc(),
        MenuItem.id.asc()
    ).all()

    home_menu_flags = {
        item.content_type: True
        for item in home_menu_items
        if item.is_visible_in_lang(current_lang)
    }

    home_titles = {
        item.content_type: item.get_title(current_lang)
        for item in home_menu_items
        if item.is_visible_in_lang(current_lang)
    }

    def get_home_title(content_type, fallback=""):
        return home_titles.get(content_type, fallback)

    home_services = Service.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(Service.display_order.asc(), Service.id.desc()).limit(6).all()

    latest_projects = Project.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(Project.display_order.asc(), Project.id.desc()).limit(4).all()

    latest_products = Product.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(Product.display_order.asc(), Product.id.desc()).limit(4).all()

    latest_posts = Post.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(Post.id.desc()).limit(4).all()

    sections = HomeSection.query.filter_by(
        is_active=True
    ).order_by(HomeSection.display_order.asc()).all()

    setting = SiteSetting.query.first()

    team_members = TeamMember.query.filter_by(
        is_active=True
    ).order_by(
        TeamMember.display_order.asc()
    ).all()

    show_partners = setting.show_partners if setting else True

    partners = Partner.query.filter_by(
        is_active=True
    ).order_by(
        Partner.display_order.asc(),
        Partner.id.desc()
    ).all()

    home_categories = Category.query.filter_by(
        is_active=True,
        show_on_home=True
    ).order_by(
        Category.display_order.asc(),
        Category.id.desc()
    ).all()

    return render_template(
        "home.html",
        home_services=home_services,
        latest_projects=latest_projects,
        latest_products=latest_products,
        latest_posts=latest_posts,
        sections=sections,
        setting=setting,
        team_members=team_members,
        home_menu_items=home_menu_items,
        home_menu_flags=home_menu_flags,
        home_titles=home_titles,
        get_home_title=get_home_title,
        partners=partners,
        show_partners=show_partners,
        home_categories=home_categories
    )

from sqlalchemy import or_
@main_bp.route("/team/<slug>")
def team_member_profile(slug):
    member = TeamMember.query.filter(
        or_(
            TeamMember.slug == slug,
            TeamMember.slug_ar == slug,
            TeamMember.slug_en == slug,
            TeamMember.slug_ja == slug
        ),
        TeamMember.is_active == True
    ).first_or_404()

    setting = SiteSetting.query.first()

    return render_template(
        "team/profile.html",
        member=member,
        setting=setting
    )

@main_bp.route("/<slug>")
def dynamic_page(slug):
    page = Page.query.filter_by(slug=slug, is_active=True).first()

    if not page:
        return "الصفحة غير موجودة", 404

    setting = SiteSetting.query.first()
    return render_template("page.html", page=page, setting=setting)

@main_bp.route("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug_ar=slug).first_or_404()
    return render_template("shop/product.html", product=product)



@main_bp.route("/ui")
def ui():
    return render_template("ui.html")
