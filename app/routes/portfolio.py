from flask import Blueprint, render_template, request, session, url_for
from sqlalchemy import or_

from app.models.project import Project


portfolio_bp = Blueprint(
    "portfolio",
    __name__,
    url_prefix="/portfolio"
)


@portfolio_bp.route("/")
def index():
    projects = (
        Project.query
        .filter_by(is_active=True)
        .order_by(
            Project.display_order.asc(),
            Project.id.asc()
        )
        .all()
    )

    return render_template(
        "portfolio/index.html",
        projects=projects
    )


@portfolio_bp.route("/<slug>")
def detail(slug):

    # اللغة الحالية للموقع
    current_lang = session.get("lang", "ar")

    # البحث عن المشروع بأي slug متوفر
    project = Project.query.filter(
        or_(
            Project.slug == slug,
            Project.slug_ar == slug,
            Project.slug_en == slug,
            Project.slug_ja == slug,
        ),
        Project.is_active == True,
    ).first_or_404()

    # =========================
    # SEO
    # =========================

    seo_title = project.get_meta_title(current_lang)

    seo_description = (
        project.get_meta_description(current_lang)
        or project.get_short_description(current_lang)
        or ""
    )

    seo_keywords = (
        project.get_keywords(current_lang)
        or ""
    )

    # صورة المشروع
    if project.image:
        seo_image = url_for(
            "static",
            filename="uploads/" + project.image,
            _external=True
        )

    elif project.images and len(project.images) > 0:
        seo_image = url_for(
            "static",
            filename="uploads/" + project.images[0].image,
            _external=True
        )

    else:
        seo_image = url_for(
            "static",
            filename="images/logo.png",
            _external=True
        )

    seo_url = request.url

    return render_template(
        "portfolio/detail.html",
        project=project,
        current_lang=current_lang,
        seo_title=seo_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords,
        seo_image=seo_image,
        seo_url=seo_url,
        seo_og_type="website",
    )