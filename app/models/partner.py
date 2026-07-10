from app import db


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)