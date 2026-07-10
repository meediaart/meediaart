from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    discount_percent = db.Column(db.Float, default=0)
    
    # ===== حقول قديمة للتوافق مع قاعدة البيانات الحالية =====
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)

    # ===== العربية =====
    title_ar = db.Column(db.String(200), nullable=False)
    slug_ar = db.Column(db.String(200), unique=True, nullable=False)
    description_ar = db.Column(db.Text)
    keywords_ar = db.Column(db.String(255))
    meta_title_ar = db.Column(db.String(255))
    meta_description_ar = db.Column(db.String(255))
    is_active_ar = db.Column(db.Boolean, default=True)

    # ===== الإنجليزية =====
    title_en = db.Column(db.String(200))
    slug_en = db.Column(db.String(200), unique=True)
    description_en = db.Column(db.Text)
    keywords_en = db.Column(db.String(255))
    meta_title_en = db.Column(db.String(255))
    meta_description_en = db.Column(db.String(255))
    is_active_en = db.Column(db.Boolean, default=True)

    # ===== اليابانية =====
    title_ja = db.Column(db.String(200))
    slug_ja = db.Column(db.String(200), unique=True)
    description_ja = db.Column(db.Text)
    keywords_ja = db.Column(db.String(255))
    meta_title_ja = db.Column(db.String(255))
    meta_description_ja = db.Column(db.String(255))
    is_active_ja = db.Column(db.Boolean, default=True)

    # ===== عامة =====
    price = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="products")

    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    show_on_home = db.Column(db.Boolean, default=False)

    # ===== خيارات المنتج =====
    has_colors = db.Column(db.Boolean, default=False)
    has_sizes = db.Column(db.Boolean, default=False)

    available_colors = db.Column(db.String(255))  # مثال: "أحمر, أزرق"
    available_sizes = db.Column(db.String(255))   # مثال: "S, M, L"

    # ===== التخصيص =====
    allow_custom_text = db.Column(db.Boolean, default=False)
    allow_custom_image = db.Column(db.Boolean, default=False)
    
    images = db.relationship(
        "ProductImage",
        backref="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.id"
    )

    def get_title(self, lang="ar"):
        return getattr(self, f"title_{lang}", None) or self.title_ar or self.title

    def get_description(self, lang="ar"):
        return getattr(self, f"description_{lang}", None) or self.description_ar or self.description

    def get_slug(self, lang="ar"):
        return getattr(self, f"slug_{lang}", None) or self.slug_ar or self.slug

    def get_keywords(self, lang="ar"):
        return getattr(self, f"keywords_{lang}", None) or self.keywords_ar

    def get_meta_title(self, lang="ar"):
        return getattr(self, f"meta_title_{lang}", None) or self.meta_title_ar or self.get_title(lang)

    def get_meta_description(self, lang="ar"):
        return getattr(self, f"meta_description_{lang}", None) or self.meta_description_ar or self.get_description(lang)

    def __repr__(self):
        return f"<Product {self.title_ar or self.title}>"