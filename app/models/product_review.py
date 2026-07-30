from app.extensions import db


class ProductReview(db.Model):
    __tablename__ = "product_reviews"

    id = db.Column(db.Integer, primary_key=True)

    # المنتج المرتبط بالتقييم
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    # بيانات العميل
    customer_name = db.Column(
        db.String(120),
        nullable=False
    )

    customer_email = db.Column(
        db.String(255),
        nullable=True
    )

    # عدد النجوم من 1 إلى 5
    rating = db.Column(
        db.Integer,
        nullable=False
    )

    # نص التعليق
    comment = db.Column(
        db.Text,
        nullable=True
    )

    # صورة يرفعها العميل
    image = db.Column(
        db.String(255),
        nullable=True
    )

    # لغة التقييم
    language = db.Column(
        db.String(5),
        default="ar",
        nullable=False
    )

    # هل وافقت الإدارة على التقييم؟
    is_approved = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # هل تظهر النجوم؟
    is_rating_visible = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # هل يظهر نص التعليق؟
    is_comment_visible = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # هل تظهر الصورة؟
    is_image_visible = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # معلومات إضافية
    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    user_agent = db.Column(
        db.String(500),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<ProductReview product_id={self.product_id} "
            f"rating={self.rating}>"
        )