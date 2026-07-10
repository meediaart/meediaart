from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    # ===== قديم للتوافق =====
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    short_description = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)

    # ===== العربية =====
    title_ar = db.Column(db.String(200), nullable=True)
    slug_ar = db.Column(db.String(200), unique=True, nullable=True)
    short_description_ar = db.Column(db.String(255), nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    keywords_ar = db.Column(db.String(255), nullable=True)
    meta_title_ar = db.Column(db.String(255), nullable=True)
    meta_description_ar = db.Column(db.String(255), nullable=True)

    # ===== الإنجليزية =====
    title_en = db.Column(db.String(200), nullable=True)
    slug_en = db.Column(db.String(200), unique=True, nullable=True)
    short_description_en = db.Column(db.String(255), nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    keywords_en = db.Column(db.String(255), nullable=True)
    meta_title_en = db.Column(db.String(255), nullable=True)
    meta_description_en = db.Column(db.String(255), nullable=True)

    # ===== اليابانية =====
    title_ja = db.Column(db.String(200), nullable=True)
    slug_ja = db.Column(db.String(200), unique=True, nullable=True)
    short_description_ja = db.Column(db.String(255), nullable=True)
    description_ja = db.Column(db.Text, nullable=True)
    keywords_ja = db.Column(db.String(255), nullable=True)
    meta_title_ja = db.Column(db.String(255), nullable=True)
    meta_description_ja = db.Column(db.String(255), nullable=True)

    # ===== عامة =====
    image = db.Column(db.String(255), nullable=True)

    client_name = db.Column(db.String(150), nullable=True)
    project_type = db.Column(db.String(150), nullable=True)

    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    show_on_home = db.Column(db.Boolean, nullable=False, default=False)

    images = db.relationship(
        "ProjectImage",
        backref="project",
        cascade="all, delete-orphan",
        order_by="ProjectImage.display_order"
    )

    def get_title(self, lang="ar"):
        return getattr(self, f"title_{lang}", None) or self.title_ar or self.title

    def get_slug(self, lang="ar"):
        return getattr(self, f"slug_{lang}", None) or self.slug_ar or self.slug

    def get_short_description(self, lang="ar"):
        return getattr(self, f"short_description_{lang}", None) or self.short_description_ar or self.short_description

    def get_description(self, lang="ar"):
        return getattr(self, f"description_{lang}", None) or self.description_ar or self.description

    def get_keywords(self, lang="ar"):
        return getattr(self, f"keywords_{lang}", None) or self.keywords_ar or self.keywords

    def get_meta_title(self, lang="ar"):
        return getattr(self, f"meta_title_{lang}", None) or self.meta_title_ar or self.meta_title or self.get_title(lang)

    def get_meta_description(self, lang="ar"):
        return getattr(self, f"meta_description_{lang}", None) or self.meta_description_ar or self.meta_description or self.get_short_description(lang)

    def __repr__(self):
        return f"<Project {self.title_ar or self.title}>"