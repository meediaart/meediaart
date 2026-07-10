from datetime import datetime
from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    # ===== قديم للتوافق =====
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)

    # ===== العربية =====
    title_ar = db.Column(db.String(200), nullable=True)
    slug_ar = db.Column(db.String(200), unique=True, nullable=True)
    excerpt_ar = db.Column(db.String(255), nullable=True)
    content_ar = db.Column(db.Text, nullable=True)
    keywords_ar = db.Column(db.String(255), nullable=True)
    meta_title_ar = db.Column(db.String(255), nullable=True)
    meta_description_ar = db.Column(db.String(255), nullable=True)

    # ===== الإنجليزية =====
    title_en = db.Column(db.String(200), nullable=True)
    slug_en = db.Column(db.String(200), unique=True, nullable=True)
    excerpt_en = db.Column(db.String(255), nullable=True)
    content_en = db.Column(db.Text, nullable=True)
    keywords_en = db.Column(db.String(255), nullable=True)
    meta_title_en = db.Column(db.String(255), nullable=True)
    meta_description_en = db.Column(db.String(255), nullable=True)

    # ===== اليابانية =====
    title_ja = db.Column(db.String(200), nullable=True)
    slug_ja = db.Column(db.String(200), unique=True, nullable=True)
    excerpt_ja = db.Column(db.String(255), nullable=True)
    content_ja = db.Column(db.Text, nullable=True)
    keywords_ja = db.Column(db.String(255), nullable=True)
    meta_title_ja = db.Column(db.String(255), nullable=True)
    meta_description_ja = db.Column(db.String(255), nullable=True)

    # ===== عامة =====
    image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    show_on_home = db.Column(db.Boolean, nullable=False, default=True)

    def get_title(self, lang="ar"):
        return getattr(self, f"title_{lang}", None) or self.title_ar or self.title

    def get_slug(self, lang="ar"):
        return getattr(self, f"slug_{lang}", None) or self.slug_ar or self.slug

    def get_excerpt(self, lang="ar"):
        return getattr(self, f"excerpt_{lang}", None) or self.excerpt_ar or self.excerpt

    def get_content(self, lang="ar"):
        return getattr(self, f"content_{lang}", None) or self.content_ar or self.content

    def get_keywords(self, lang="ar"):
        return getattr(self, f"keywords_{lang}", None) or self.keywords_ar or self.keywords

    def get_meta_title(self, lang="ar"):
        return getattr(self, f"meta_title_{lang}", None) or self.meta_title_ar or self.meta_title or self.get_title(lang)

    def get_meta_description(self, lang="ar"):
        return getattr(self, f"meta_description_{lang}", None) or self.meta_description_ar or self.meta_description or self.get_excerpt(lang)

    def __repr__(self):
        return f"<Post {self.title_ar or self.title}>"