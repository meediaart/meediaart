from flask import Blueprint, render_template, session
from sqlalchemy import or_

from app.models.service import Service
from app.models.settings import SiteSetting

services_bp = Blueprint("services", __name__, url_prefix="/services")


@services_bp.route("/")
def index():
    services = Service.query.filter_by(
        is_active=True
    ).order_by(
        Service.display_order.asc(),
        Service.id.asc()
    ).all()

    setting = SiteSetting.query.first()

    return render_template(
        "services/index.html",
        services=services,
        setting=setting
    )


@services_bp.route("/<slug>")
def detail(slug):
    current_lang = session.get("lang", "ar")

    service = Service.query.filter(
        or_(
            Service.slug_ar == slug,
            Service.slug_en == slug,
            Service.slug_ja == slug
        )
    ).first_or_404()

    related_services = Service.query.filter(
        Service.id != service.id,
        Service.is_active == True
    ).order_by(
        Service.display_order.asc(),
        Service.id.asc()
    ).limit(5).all()

    return render_template(
        "services/detail.html",
        service=service,
        related_services=related_services,
        current_lang=current_lang
    )