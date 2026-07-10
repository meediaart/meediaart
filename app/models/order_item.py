from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100))
    size = db.Column(db.String(100))
    custom_text = db.Column(db.Text)
    custom_image = db.Column(db.String(255))

    order = db.relationship("Order", back_populates="items")

    def __repr__(self):
        return f"<OrderItem {self.product_title}>"