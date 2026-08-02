from flask import Blueprint, render_template
from app.utils.seo import build_seo

from app.models.settings import SiteSetting
from app.models.team_member import TeamMember

about_bp = Blueprint("about", __name__, url_prefix="/about")


@about_bp.route("/")
def index():
    members = TeamMember.query.filter_by(
        is_active=True
    ).order_by(
        TeamMember.display_order.asc(),
        TeamMember.id.asc()
    ).all()

    setting = SiteSetting.query.first()

    seo = build_seo(
        title="About Us | MEDIA ART",
        description=(
            "Learn more about MEDIA ART, our team, "
            "our vision and our professional digital services."
        ),
        keywords=(
            "media art, about us, web design, "
            "digital marketing, printing, branding"
        ),
    )

    return render_template(
        "about/index.html",
        members=members,
        setting=setting,
        **seo,
    )