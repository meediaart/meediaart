from app.extensions import db


class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    payment_type = db.Column(
        db.String(50),
        nullable=False
    )

    provider = db.Column(
        db.String(100)
    )

    account_name = db.Column(
        db.String(150)
    )

    account_number = db.Column(
        db.String(100)
    )

    is_default = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    user = db.relationship(
    "User",
    back_populates="payment_methods"
    )