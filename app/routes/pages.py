from flask import Blueprint, render_template, session

from app.models.page import Page

pages_bp = Blueprint("pages", __name__, url_prefix="/pages")


@pages_bp.route("/<slug>")
def page_detail(slug):
    current_lang = session.get("lang", "ar")

    page = Page.query.filter(
        (
            (Page.slug_ar == slug) |
            (Page.slug_en == slug) |
            (Page.slug_ja == slug)
        ),
        Page.is_active == True
    ).first_or_404()

    return render_template(
        "pages/detail.html",
        page=page,
        current_lang=current_lang
    )