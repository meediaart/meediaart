from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("orders", lazy=True)
    )

    customer_name = db.Column(db.String(150), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=True)
    customer_address = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(10), default="ar")

    total_price = db.Column(db.Float, nullable=False, default=0.0)

    status = db.Column(db.String(50), nullable=False, default="pending")
    payment_method = db.Column(db.String(50), nullable=False, default="cod")
    payment_status = db.Column(db.String(50), nullable=False, default="unpaid")
    stripe_session_id = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order {self.id}>"