from app.extensions import db


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    postal_code = db.Column(db.String(20))
    prefecture = db.Column(db.String(100))
    city = db.Column(db.String(150))
    address_line = db.Column(db.String(255), nullable=False)
    building = db.Column(db.String(255))

    is_default = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    user = db.relationship(
    "User",
    back_populates="addresses"
    )