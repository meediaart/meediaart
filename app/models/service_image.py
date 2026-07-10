from app import db

class ServiceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)