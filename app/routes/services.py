from flask import Blueprint, render_template, session, url_for
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
        ),
        Service.is_active == True,
    ).first_or_404()

    related_services = Service.query.filter(
        Service.id != service.id,
        Service.is_active == True
    ).order_by(
        Service.display_order.asc(),
        Service.id.asc()
    ).limit(5).all()

    # =========================
    # SEO الخاص بالخدمة
    # =========================

    seo_title = service.get_meta_title(current_lang)

    seo_description = (
        service.get_meta_description(current_lang)
        or service.get_short_description(current_lang)
        or ""
    )

    seo_keywords = (
        service.get_keywords(current_lang)
        or ""
    )

    if service.image:
        seo_image = url_for(
            "static",
            filename="uploads/" + service.image,
            _external=True,
        )

    elif service.images and len(service.images) > 0:
        seo_image = url_for(
            "static",
            filename="uploads/" + service.images[0].image,
            _external=True,
        )

    else:
        seo_image = url_for(
            "static",
            filename="images/logo.png",
            _external=True,
        )

    seo_url = url_for(
        "services.detail",
        slug=service.get_slug(current_lang),
        _external=True,
    )

    return render_template(
        "services/detail.html",
        service=service,
        related_services=related_services,
        current_lang=current_lang,

        seo_title=seo_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords,
        seo_image=seo_image,
        seo_url=seo_url,
        seo_og_type="website",
    )