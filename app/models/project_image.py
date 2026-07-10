from app import db

class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)