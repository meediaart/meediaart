from flask import Blueprint, render_template

from app.models.project import Project

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@portfolio_bp.route("/")
def index():
    projects = Project.query.order_by(Project.id.asc()).all()
    return render_template("portfolio/index.html", projects=projects)


@portfolio_bp.route("/<slug>")
def detail(slug):
    project = Project.query.filter_by(slug=slug).first()

    if not project:
        return render_template("portfolio/detail.html", project=None), 404

    return render_template("portfolio/detail.html", project=project)