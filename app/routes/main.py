from datetime import datetime, timezone

from flask import (
    Blueprint,
    Response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models.category import Category
from app.models.home_section import HomeSection
from app.models.menu_item import MenuItem
from app.models.page import Page
from app.models.partner import Partner
from app.models.post import Post
from app.models.product import Product
from app.models.project import Project
from app.models.service import Service
from app.models.settings import SiteSetting
from app.models.team_member import TeamMember

main_bp = Blueprint("main", __name__)

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
    
    seo_title = (
        setting.site_name
        if setting and setting.site_name
        else "MEDIA ART"
    )

    seo_description = (
        setting.site_description
        if setting and getattr(setting, "site_description", None)
        else "MEDIA ART - Professional Web Design, Branding, Printing, Digital Marketing and IT Solutions."
    )

    seo_keywords = (
        "media art, web design, web development, branding, printing, "
        "digital marketing, ecommerce, seo, japan"
    )

    seo_image = (
        url_for(
            "static",
            filename="images/logo.png",
            _external=True,
        )
    )

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
        home_categories=home_categories,
        seo_title=seo_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords,
        seo_image=seo_image,
        seo_url=request.url,
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
    return redirect(
        url_for("pages.page_detail", slug=slug),
        code=301
    )

@main_bp.route("/product/<slug>")
def product_detail(slug):
    return redirect(
        url_for("shop.product", slug=slug),
        code=301
    )
    
    
@main_bp.route("/sitemap.xml")
def sitemap():

    pages = []
    today = datetime.now(timezone.utc).date().isoformat()

    def add_static(endpoint, priority="0.8", changefreq="weekly"):
        pages.append({
            "loc": url_for(endpoint, _external=True),
            "lastmod": today,
            "priority": priority,
            "changefreq": changefreq
        })

    def add_dynamic(items, endpoint, slug_field,
                    priority="0.8",
                    changefreq="monthly"):

        for item in items:

            slug = getattr(item, slug_field, None)

            if not slug:
                continue

            pages.append({
                "loc": url_for(
                    endpoint,
                    slug=slug,
                    _external=True
                ),
                "lastmod": today,
                "priority": priority,
                "changefreq": changefreq
            })

    # ========= الصفحات الرئيسية =========

    add_static("main.home", "1.0", "daily")
    add_static("about.index", "0.8", "monthly")
    add_static("services.index", "0.9", "weekly")
    add_static("portfolio.index", "0.9", "weekly")
    add_static("shop.index", "0.9", "daily")
    add_static("blog.index", "0.8", "daily")
    add_static("contact.index", "0.6", "monthly")

    # ========= الصفحات الديناميكية =========

    add_dynamic(
        Page.query.filter_by(is_active=True).all(),
        "pages.page_detail",
        "slug",
        "0.7",
        "monthly"
    )

    add_dynamic(
        Service.query.filter_by(is_active=True).all(),
        "services.detail",
        "slug_ar",
        "0.8",
        "monthly"
    )

    add_dynamic(
        Project.query.filter_by(is_active=True).all(),
        "portfolio.detail",
        "slug_ar",
        "0.8",
        "monthly"
    )

    add_dynamic(
    Product.query.filter_by(is_active=True).all(),
    "shop.product",
    "slug_ar",
    "0.8",
    "weekly"
    )

    add_dynamic(
        Post.query.filter_by(is_active=True).all(),
        "blog.article",
        "slug_ar",
        "0.7",
        "monthly"
    )

    xml = render_template(
        "sitemap.xml",
        pages=pages
    )

    return Response(
        xml,
        mimetype="application/xml"
    )

@main_bp.route("/ui")
def ui():
    return render_template("ui.html")
