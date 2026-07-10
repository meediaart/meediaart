from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # استيراد وتسجيل الـ blueprints
    from app.routes.main import main_bp
    from app.routes.about import about_bp
    from app.routes.services import services_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.shop import shop_bp
    from app.routes.blog import blog_bp
    from app.routes.contact import contact_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    return app