from datetime import datetime

from app.extensions import db


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=True)

    language = db.Column(db.String(10), default="ar")
    source = db.Column(db.String(50), default="website")

    consent_given = db.Column(db.Boolean, default=False)
    consent_at = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(100), nullable=True)

    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Subscriber {self.email}>"