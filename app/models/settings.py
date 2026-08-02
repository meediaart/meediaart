from app.extensions import db


class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    site_name = db.Column(db.String(200))
    logo = db.Column(db.String(200))
    footer_text = db.Column(db.String(300))
    show_partners = db.Column(db.Boolean, default=True)