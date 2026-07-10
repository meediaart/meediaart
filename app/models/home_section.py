from app.extensions import db


class HomeSection(db.Model):
    __tablename__ = "home_sections"

    id = db.Column(db.Integer, primary_key=True)

    # ===== قديم للتوافق =====
    title = db.Column(db.String(200), nullable=True)
    subtitle = db.Column(db.Text, nullable=True)
    button_text = db.Column(db.String(100), nullable=True)

    # ===== العربية =====
    title_ar = db.Column(db.String(200))
    subtitle_ar = db.Column(db.Text)
    button_text_ar = db.Column(db.String(100))

    # ===== الإنجليزية =====
    title_en = db.Column(db.String(200))
    subtitle_en = db.Column(db.Text)
    button_text_en = db.Column(db.String(100))

    # ===== اليابانية =====
    title_ja = db.Column(db.String(200))
    subtitle_ja = db.Column(db.Text)
    button_text_ja = db.Column(db.String(100))

    # ===== عامة =====
    button_link = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)

    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # =========================
    # HELPERS
    # =========================

    def get_title(self, lang="ar"):
        return getattr(self, f"title_{lang}", None) or self.title_ar or self.title

    def get_subtitle(self, lang="ar"):
        return getattr(self, f"subtitle_{lang}", None) or self.subtitle_ar or self.subtitle

    def get_button_text(self, lang="ar"):
        return getattr(self, f"button_text_{lang}", None) or self.button_text_ar or self.button_text

    def __repr__(self):
        return f"<HomeSection {self.title_ar or self.title}>"