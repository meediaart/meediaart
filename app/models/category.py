from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)

    image = db.Column(db.String(255))

    name_ar = db.Column(db.String(150))
    slug_ar = db.Column(db.String(150), unique=True)
    description_ar = db.Column(db.Text)
    keywords_ar = db.Column(db.String(255))
    meta_title_ar = db.Column(db.String(255))
    meta_description_ar = db.Column(db.String(255))

    name_en = db.Column(db.String(150))
    slug_en = db.Column(db.String(150), unique=True)
    description_en = db.Column(db.Text)
    keywords_en = db.Column(db.String(255))
    meta_title_en = db.Column(db.String(255))
    meta_description_en = db.Column(db.String(255))

    name_ja = db.Column(db.String(150))
    slug_ja = db.Column(db.String(150), unique=True)
    description_ja = db.Column(db.Text)
    keywords_ja = db.Column(db.String(255))
    meta_title_ja = db.Column(db.String(255))
    meta_description_ja = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, default=True)
    show_on_home = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)

    products = db.relationship("Product", back_populates="category", lazy=True)
    
    def get_name(self, lang="ar"):
        return getattr(self, f"name_{lang}", None) or self.name_ar or self.name

    def get_slug(self, lang="ar"):
        return getattr(self, f"slug_{lang}", None) or self.slug_ar or self.slug

    def get_description(self, lang="ar"):
        return getattr(self, f"description_{lang}", None) or self.description_ar

    def get_keywords(self, lang="ar"):
        return getattr(self, f"keywords_{lang}", None) or self.keywords_ar

    def get_meta_title(self, lang="ar"):
        return getattr(self, f"meta_title_{lang}", None) or self.meta_title_ar or self.get_name(lang)

    def get_meta_description(self, lang="ar"):
        return getattr(self, f"meta_description_{lang}", None) or self.meta_description_ar or self.get_description(lang)

    def __repr__(self):
        return f"<Category {self.name}>"