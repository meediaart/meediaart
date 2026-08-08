import re

from flask import Blueprint, render_template, session, url_for

from app.models.page import Page

pages_bp = Blueprint("pages", __name__, url_prefix="/pages")


@pages_bp.route("/<slug>")
def page_detail(slug):
    current_lang = session.get("lang", "ar")

    page = Page.query.filter(
        (
            (Page.slug == slug) |
            (Page.slug_ar == slug) |
            (Page.slug_en == slug) |
            (Page.slug_ja == slug)
        ),
        Page.is_active == True
    ).first_or_404()

    # =========================
    # بيانات الصفحة حسب اللغة
    # =========================

    if current_lang == "en":
        page_title = page.title_en or page.title_ar or page.title

        page_content = (
            page.content_en
            or page.content_ar
            or page.content
            or ""
        )

        page_slug = page.slug_en or page.slug_ar or page.slug

    elif current_lang == "ja":
        page_title = page.title_ja or page.title_ar or page.title

        page_content = (
            page.content_ja
            or page.content_ar
            or page.content
            or ""
        )

        page_slug = page.slug_ja or page.slug_ar or page.slug

    else:
        page_title = page.title_ar or page.title

        page_content = (
            page.content_ar
            or page.content
            or ""
        )

        page_slug = page.slug_ar or page.slug

    # =========================
    # SEO
    # =========================

    # إزالة وسوم HTML من المحتوى
    seo_description = re.sub(r"<[^>]+>", " ", page_content)

    # ترتيب المسافات والأسطر
    seo_description = re.sub(r"\s+", " ", seo_description).strip()

    # وصف مختصر لمحركات البحث
    seo_description = seo_description[:160]

    seo_url = url_for(
        "pages.page_detail",
        slug=page_slug,
        _external=True,
    )

    seo_image = url_for(
        "static",
        filename="images/logo.png",
        _external=True,
    )

    return render_template(
        "pages/detail.html",
        page=page,
        current_lang=current_lang,

        page_title=page_title,
        page_content=page_content,

        seo_title=page_title,
        seo_description=seo_description,
        seo_url=seo_url,
        seo_image=seo_image,
    )