from flask import Blueprint, render_template
from app.models.team_member import TeamMember
from app.models.settings import SiteSetting

about_bp = Blueprint("about", __name__, url_prefix="/about")


@about_bp.route("/")
def index():
    members = TeamMember.query.filter_by(
        is_active=True
    ).order_by(TeamMember.display_order.asc(), TeamMember.id.asc()).all()

    setting = SiteSetting.query.first()

    return render_template("about/index.html", members=members, setting=setting)