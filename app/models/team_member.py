from app.extensions import db


class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)

    # =========================
    # العربية
    # =========================
    name_ar = db.Column(db.String(150), nullable=False)
    slug_ar = db.Column(db.String(150), unique=True, nullable=False)
    job_title_ar = db.Column(db.String(150), nullable=True)
    short_bio_ar = db.Column(db.Text, nullable=True)
    full_bio_ar = db.Column(db.Text, nullable=True)

    # =========================
    # الإنجليزية
    # =========================
    name_en = db.Column(db.String(150), nullable=True)
    slug_en = db.Column(db.String(150), unique=True, nullable=True)
    job_title_en = db.Column(db.String(150), nullable=True)
    short_bio_en = db.Column(db.Text, nullable=True)
    full_bio_en = db.Column(db.Text, nullable=True)

    # =========================
    # اليابانية
    # =========================
    name_ja = db.Column(db.String(150), nullable=True)
    slug_ja = db.Column(db.String(150), unique=True, nullable=True)
    job_title_ja = db.Column(db.String(150), nullable=True)
    short_bio_ja = db.Column(db.Text, nullable=True)
    full_bio_ja = db.Column(db.Text, nullable=True)

    # =========================
    # التوافق القديم
    # =========================
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    job_title = db.Column(db.String(150), nullable=True)
    short_bio = db.Column(db.Text, nullable=True)
    full_bio = db.Column(db.Text, nullable=True)

    # =========================
    # بيانات عامة
    # =========================
    image = db.Column(db.String(255), nullable=True)

    display_order = db.Column(db.Integer, nullable=False, default=0)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    show_on_home = db.Column(db.Boolean, default=False)

    # =========================
    # Helpers
    # =========================
    def get_name(self, lang="ar"):
        if lang == "en" and self.name_en:
            return self.name_en

        if lang == "ja" and self.name_ja:
            return self.name_ja

        return self.name_ar or self.name

    def get_slug(self, lang="ar"):
        if lang == "en" and self.slug_en:
            return self.slug_en

        if lang == "ja" and self.slug_ja:
            return self.slug_ja

        return self.slug_ar or self.slug

    def get_job_title(self, lang="ar"):
        if lang == "en" and self.job_title_en:
            return self.job_title_en

        if lang == "ja" and self.job_title_ja:
            return self.job_title_ja

        return self.job_title_ar or self.job_title

    def get_short_bio(self, lang="ar"):
        if lang == "en" and self.short_bio_en:
            return self.short_bio_en

        if lang == "ja" and self.short_bio_ja:
            return self.short_bio_ja

        return self.short_bio_ar or self.short_bio

    def get_full_bio(self, lang="ar"):
        if lang == "en" and self.full_bio_en:
            return self.full_bio_en

        if lang == "ja" and self.full_bio_ja:
            return self.full_bio_ja

        return self.full_bio_ar or self.full_bio

    def __repr__(self):
        return f"<TeamMember {self.name_ar}>"