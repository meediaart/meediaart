from flask import Flask, session, url_for, redirect, request
from config import Config

from app.extensions import db, login_manager, mail, babel
from app.routes.newsletter import newsletter_bp
from app.routes.pages import pages_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    def get_locale():

        lang = session.get("lang", "ar")

        if lang in ["ar", "en", "ja"]:
            return lang

        return "ar"

    babel.init_app(
        app,
        locale_selector=get_locale
    )

    @app.context_processor
    def inject_settings():

        from app.models import SiteSetting

        setting = SiteSetting.query.first()

        return {
            "setting": setting
        }

    with app.app_context():

        from app.models import (
            Service,
            Post,
            Product,
            ProductReview,
            Category,
            Project,
            User,
            Order,
            MenuItem,
            Page,
            HomeSection,
            SiteSetting,
            ContactMessage,
            Favorite,
        )

        db.create_all()

    from app.routes.main import main_bp
    from app.routes.about import about_bp
    from app.routes.services import services_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.shop import shop_bp
    from app.routes.blog import blog_bp
    from app.routes.contact import contact_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.customer_auth import customer_auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(newsletter_bp)
    app.register_blueprint(customer_auth_bp)
    app.register_blueprint(pages_bp)

    @app.context_processor
    def inject_menu_items():

        from app.models.menu_item import MenuItem

        items = (
            MenuItem.query
            .filter_by(is_active=True)
            .order_by(
                MenuItem.display_order.asc(),
                MenuItem.id.asc()
            )
            .all()
        )

        def resolve_menu_url(item):

            if item.content_type == "home":
                return url_for("main.home")

            elif item.content_type == "about":
                return url_for("about.index")

            elif item.content_type == "services":
                return url_for("services.index")

            elif item.content_type == "portfolio":
                return url_for("portfolio.index")

            elif item.content_type == "shop":
                return url_for("shop.index")

            elif item.content_type == "blog":
                return url_for("blog.index")

            elif item.content_type == "contact":
                return url_for("contact.index")

            elif item.content_type == "page":

                if item.page:
                    return url_for(
                        "pages.page_detail",
                        slug=item.page.slug
                    )

                elif item.endpoint:
                    return url_for(
                        "pages.page_detail",
                        slug=item.endpoint
                    )

            elif (
                item.content_type == "external"
                and item.custom_url
            ):
                return item.custom_url

            elif item.endpoint:
                return url_for(item.endpoint)

            elif item.custom_url:
                return item.custom_url

            return "#"

        return {
            "main_menu_items": items,
            "resolve_menu_url": resolve_menu_url
        }

    @app.context_processor
    def inject_pages():

        from app.models.page import Page

        menu_pages = (
            Page.query
            .filter_by(
                is_active=True,
                show_in_menu=True
            )
            .order_by(
                Page.display_order.asc(),
                Page.id.asc()
            )
            .all()
        )

        footer_pages = (
            Page.query
            .filter_by(
                is_active=True,
                show_in_footer=True
            )
            .order_by(
                Page.display_order.asc(),
                Page.id.asc()
            )
            .all()
        )

        return {
            "menu_pages": menu_pages,
            "footer_pages": footer_pages
        }

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    @app.context_processor
    def inject_globals():

        current_lang = session.get("lang", "ar")

        translations = {
            "ar": {
                "home": "الرئيسية",
                "about": "من نحن",
                "services": "الخدمات",
                "shop": "المتجر",
                "contact": "تواصل معنا",
                "team": "فريق العمل",
                "read_more": "قراءة المزيد",
                "read_bio": "قراءة السيرة الذاتية",
                "featured_services": "الخدمات المميزة",
                "site_default": "موقعي",
                "request_service": "اطلب خدمة",
                "quick_links": "روابط سريعة",
                "footer_text": (
                    "حلول متكاملة في التصميم، والطباعة، "
                    "والتسويق الرقمي لبناء حضور قوي "
                    "لعلامتك التجارية."
                ),
                "email": "البريد",
                "phone": "الهاتف",
                "address": "العنوان",
                "japan": "اليابان",
                "rights": "جميع الحقوق محفوظة",
                "portfolio": "أعمالنا",
                "blog": "المدونة"
            },

            "en": {
                "home": "Home",
                "about": "About Us",
                "services": "Services",
                "shop": "Shop",
                "contact": "Contact Us",
                "team": "Our Team",
                "read_more": "Read More",
                "read_bio": "Read Biography",
                "featured_services": "Featured Services",
                "site_default": "My Website",
                "request_service": "Request Service",
                "quick_links": "Quick Links",
                "footer_text": (
                    "Integrated solutions in design, printing, "
                    "and digital marketing to build a strong "
                    "presence for your brand."
                ),
                "email": "Email",
                "phone": "Phone",
                "address": "Address",
                "japan": "Japan",
                "rights": "All rights reserved",
                "portfolio": "Portfolio",
                "blog": "Blog"
            },

            "ja": {
                "home": "ホーム",
                "about": "会社概要",
                "services": "サービス",
                "shop": "ショップ",
                "contact": "お問い合わせ",
                "team": "チーム",
                "read_more": "続きを読む",
                "read_bio": "プロフィールを見る",
                "featured_services": "注目サービス",
                "site_default": "マイサイト",
                "request_service": "サービスを依頼",
                "quick_links": "クイックリンク",
                "footer_text": (
                    "デザイン、印刷、デジタルマーケティングを通じて、"
                    "ブランドの存在感を高める総合ソリューションを"
                    "提供します。"
                ),
                "email": "メール",
                "phone": "電話",
                "address": "住所",
                "japan": "日本",
                "rights": "全著作権所有",
                "portfolio": "制作実績",
                "blog": "ブログ"
            }
        }

        return {
            "current_lang": current_lang,
            "tr": translations.get(
                current_lang,
                translations["ar"]
            )
        }

    @app.route("/set-language/<lang>")
    def set_language(lang):

        if lang in ["ar", "en", "ja"]:
            session["lang"] = lang

        return redirect(
            request.referrer
            or url_for("main.home")
        )

    return app