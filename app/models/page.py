from app.extensions import db


class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)

    # ===== العناوين =====
    title = db.Column(db.String(150), nullable=False)  # مؤقتًا للتوافق مع النظام الحالي
    title_ar = db.Column(db.String(150))
    title_en = db.Column(db.String(150))
    title_ja = db.Column(db.String(150))

    # ===== الروابط =====
    slug = db.Column(db.String(150), unique=True, nullable=False)  # مؤقتًا
    slug_ar = db.Column(db.String(150), unique=True)
    slug_en = db.Column(db.String(150), unique=True)
    slug_ja = db.Column(db.String(150), unique=True)

    # ===== المحتوى =====
    content = db.Column(db.Text, nullable=False)
    
    content_ar = db.Column(db.Text)
    content_en = db.Column(db.Text)
    content_ja = db.Column(db.Text)

    # ===== نوع الصفحة =====
    page_type = db.Column(
        db.String(20),
        default="main"
    )  # main / child

    # ===== الصفحة الأم =====
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("pages.id"),
        nullable=True
    )

    parent = db.relationship(
        "Page",
        remote_side=[id],
        backref="children"
    )

    # ===== القالب =====
    template = db.Column(
        db.String(100),
        default="default"
    )

    # ===== أماكن الظهور =====
    show_in_menu = db.Column(
        db.Boolean,
        default=True
    )

    show_on_home = db.Column(
        db.Boolean,
        default=False
    )

    show_in_footer = db.Column(
        db.Boolean,
        default=False
    )

    # ===== الترتيب =====
    display_order = db.Column(
        db.Integer,
        default=0
    )

    # ===== الحالة =====
    is_active = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):
        return f"<Page {self.title}>"