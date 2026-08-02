from app.extensions import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    # العربية
    title_ar = db.Column(db.String(200), nullable=False)
    slug_ar = db.Column(db.String(200), unique=True, nullable=False)
    short_description_ar = db.Column(db.String(255), nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    keywords_ar = db.Column(db.String(255), nullable=True)
    meta_title_ar = db.Column(db.String(255), nullable=True)
    meta_description_ar = db.Column(db.String(255), nullable=True)
    is_active_ar = db.Column(db.Boolean, nullable=False, default=True)

    # الإنجليزية
    title_en = db.Column(db.String(200), nullable=True)
    slug_en = db.Column(db.String(200), nullable=True)
    short_description_en = db.Column(db.String(255), nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    keywords_en = db.Column(db.String(255), nullable=True)
    meta_title_en = db.Column(db.String(255), nullable=True)
    meta_description_en = db.Column(db.String(255), nullable=True)
    is_active_en = db.Column(db.Boolean, nullable=False, default=True)

    # اليابانية
    title_ja = db.Column(db.String(200), nullable=True)
    slug_ja = db.Column(db.String(200), nullable=True)
    short_description_ja = db.Column(db.String(255), nullable=True)
    description_ja = db.Column(db.Text, nullable=True)
    keywords_ja = db.Column(db.String(255), nullable=True)
    meta_title_ja = db.Column(db.String(255), nullable=True)
    meta_description_ja = db.Column(db.String(255), nullable=True)
    is_active_ja = db.Column(db.Boolean, nullable=False, default=True)

    # عامة
    image = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    booking_link = db.Column(db.String(255), nullable=True)

    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    show_on_home = db.Column(db.Boolean, nullable=False, default=False)

    
    images = db.relationship(
        "ServiceImage",
        backref="service",
        cascade="all, delete-orphan",
        order_by="ServiceImage.display_order"
    )

    def get_title(self, lang="ar"):
        if lang == "en" and self.title_en:
            return self.title_en
        if lang == "ja" and self.title_ja:
            return self.title_ja
        return self.title_ar

    def get_short_description(self, lang="ar"):
        if lang == "en" and self.short_description_en:
            return self.short_description_en
        if lang == "ja" and self.short_description_ja:
            return self.short_description_ja
        return self.short_description_ar

    def get_description(self, lang="ar"):
        if lang == "en" and self.description_en:
            return self.description_en
        if lang == "ja" and self.description_ja:
            return self.description_ja
        return self.description_ar

    def get_slug(self, lang="ar"):
        if lang == "en" and self.slug_en:
            return self.slug_en
        if lang == "ja" and self.slug_ja:
            return self.slug_ja
        return self.slug_ar

    def get_meta_title(self, lang="ar"):
        if lang == "en" and self.meta_title_en:
            return self.meta_title_en
        if lang == "ja" and self.meta_title_ja:
            return self.meta_title_ja
        return self.meta_title_ar or self.title_ar

    def get_meta_description(self, lang="ar"):
        if lang == "en" and self.meta_description_en:
            return self.meta_description_en
        if lang == "ja" and self.meta_description_ja:
            return self.meta_description_ja
        return self.meta_description_ar or self.short_description_ar

    def __repr__(self):
        return f"<Service {self.title_ar}>"