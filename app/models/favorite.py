from app.extensions import db


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref("favorites", cascade="all, delete-orphan")
    )

    product = db.relationship(
        "Product",
        backref=db.backref("favorited_by", cascade="all, delete-orphan")
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_user_product_favorite"),
    )

    def __repr__(self):
        return f"<Favorite user={self.user_id} product={self.product_id}>"