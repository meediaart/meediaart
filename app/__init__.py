from flask import Flask, redirect, request, session, url_for

from app.extensions import babel, db, login_manager, mail
from app.routes.newsletter import newsletter_bp
from app.routes.pages import pages_bp
from config import Config


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

        from app import models  # noqa: F401

        db.create_all()

        

    from app.routes.about import about_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.blog import blog_bp
    from app.routes.contact import contact_bp
    from app.routes.customer_auth import customer_auth_bp
    from app.routes.main import main_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.services import services_bp
    from app.routes.shop import shop_bp

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

        from app.models import User

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
        "blog": "المدونة",

        "my_account": "حسابي",
        "profile": "الملف الشخصي",
        "addresses": "العناوين",
        "payment_methods": "طرق الدفع",
        "orders": "طلباتي",
        "favorites": "المفضلة",
        "security": "الأمان",
        "logout": "تسجيل الخروج",

        "personal_information": "المعلومات الشخصية",
        "username": "اسم المستخدم",
        "first_name": "الاسم الأول",
        "last_name": "اسم العائلة",
        "full_name": "الاسم الكامل",

        "edit": "تعديل",
        "delete": "حذف",
        "save": "حفظ",
        "cancel": "إلغاء",

        "add_new_address": "إضافة عنوان جديد",
        "default_address": "العنوان الافتراضي",
        "set_default": "تعيين كافتراضي",

        "postal_code": "الرمز البريدي",
        "prefecture": "المحافظة",
        "city": "المدينة",
        "building": "المبنى",

        "edit_profile": "تعديل الملف الشخصي",
        "email_address": "البريد الإلكتروني",
        "phone_number": "رقم الهاتف",
        "no_addresses": "لا يوجد أي عنوان حتى الآن.",
        "delete_confirmation": "هل تريد حذف هذا العنوان؟",
        "default": "افتراضي",
        "add_payment_method": "إضافة طريقة دفع",
        "no_payment_methods": "لا توجد طرق دفع محفوظة.",
        "provider": "مزود الخدمة",
        "account_number": "رقم الحساب",
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
        "blog": "Blog",

        "my_account": "My Account",
        "profile": "Profile",
        "addresses": "Addresses",
        "payment_methods": "Payment Methods",
        "orders": "My Orders",
        "favorites": "Favorites",
        "security": "Security",
        "logout": "Logout",

        "personal_information": "Personal Information",
        "username": "Username",
        "first_name": "First Name",
        "last_name": "Last Name",
        "full_name": "Full Name",

        "edit": "Edit",
        "delete": "Delete",
        "save": "Save",
        "cancel": "Cancel",

        "add_new_address": "Add New Address",
        "default_address": "Default Address",
        "set_default": "Set as Default",

        "postal_code": "Postal Code",
        "prefecture": "Prefecture",
        "city": "City",
        "building": "Building",

        "edit_profile": "Edit Profile",
        "email_address": "Email Address",
        "phone_number": "Phone Number",
        "no_addresses": "No addresses found.",
        "delete_confirmation": "Are you sure you want to delete this address?",
        "default": "Default",
        "add_payment_method": "Add Payment Method",
        "no_payment_methods": "No payment methods found.",
        "provider": "Provider",
        "account_number": "Account Number",
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
        "blog": "ブログ",

        "my_account": "マイアカウント",
        "profile": "プロフィール",
        "addresses": "住所",
        "payment_methods": "支払い方法",
        "orders": "注文履歴",
        "favorites": "お気に入り",
        "security": "セキュリティ",
        "logout": "ログアウト",

        "personal_information": "個人情報",
        "username": "ユーザー名",
        "first_name": "名",
        "last_name": "姓",
        "full_name": "氏名",

        "edit": "編集",
        "delete": "削除",
        "save": "保存",
        "cancel": "キャンセル",

        "add_new_address": "新しい住所を追加",
        "default_address": "デフォルト住所",
        "set_default": "デフォルトに設定",

        "postal_code": "郵便番号",
        "prefecture": "都道府県",
        "city": "市区町村",
        "building": "建物名",

        "edit_profile": "プロフィールを編集",
        "email_address": "メールアドレス",
        "phone_number": "電話番号",
        "no_addresses": "住所が登録されていません。",
        "delete_confirmation": "この住所を削除してもよろしいですか？",
        "default": "デフォルト",
        "add_payment_method": "支払い方法を追加",
        "no_payment_methods": "保存された支払い方法はありません。",
        "provider": "サービス提供会社",
        "account_number": "口座番号",
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