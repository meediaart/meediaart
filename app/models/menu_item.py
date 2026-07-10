from app.extensions import db


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)

    # ===== قديم للتوافق =====
    title = db.Column(db.String(100), nullable=False)

    # ===== اللغات =====
    title_ar = db.Column(db.String(100), nullable=True)
    title_en = db.Column(db.String(100), nullable=True)
    title_ja = db.Column(db.String(100), nullable=True)

    is_active_ar = db.Column(db.Boolean, nullable=False, default=True)
    is_active_en = db.Column(db.Boolean, nullable=False, default=True)
    is_active_ja = db.Column(db.Boolean, nullable=False, default=True)

    # ===== الرابط =====
    content_type = db.Column(db.String(50), nullable=True)
    endpoint = db.Column(db.String(100), nullable=True)
    custom_url = db.Column(db.String(255), nullable=True)

    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    show_on_home = db.Column(db.Boolean, default=False)

    def get_title(self, lang="ar"):
        return getattr(self, f"title_{lang}", None) or self.title_ar or self.title

    def is_visible_in_lang(self, lang="ar"):
        return getattr(self, f"is_active_{lang}", True)

    def __repr__(self):
        return f"<MenuItem {self.title_ar or self.title}>"