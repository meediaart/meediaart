from app.extensions import db


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)

    # ==========================
    # العناوين
    # ==========================

    title = db.Column(db.String(100), nullable=False)

    title_ar = db.Column(db.String(100))
    title_en = db.Column(db.String(100))
    title_ja = db.Column(db.String(100))

    is_active_ar = db.Column(db.Boolean, default=True, nullable=False)
    is_active_en = db.Column(db.Boolean, default=True, nullable=False)
    is_active_ja = db.Column(db.Boolean, default=True, nullable=False)

    # ==========================
    # نوع الرابط
    # ==========================

    content_type = db.Column(db.String(50))

    endpoint = db.Column(db.String(100))

    custom_url = db.Column(db.String(255))

    # الصفحة المرتبطة
    page_id = db.Column(
        db.Integer,
        db.ForeignKey("pages.id"),
        nullable=True
    )

    page = db.relationship(
        "Page",
        backref="menu_items"
    )

    # ==========================
    # الإعدادات
    # ==========================

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    show_on_home = db.Column(
        db.Boolean,
        default=False
    )

    # ==========================
    # المساعدات
    # ==========================

    def get_title(self, lang="ar"):

        if self.page:

            if lang == "en":
                return self.page.title_en or self.page.title_ar

            if lang == "ja":
                return self.page.title_ja or self.page.title_ar

            return self.page.title_ar

        return (
            getattr(self, f"title_{lang}", None)
            or self.title_ar
            or self.title
        )

    def is_visible_in_lang(self, lang="ar"):
        return getattr(
            self,
            f"is_active_{lang}",
            True
        )

    def __repr__(self):
        return f"<MenuItem {self.get_title()}>"