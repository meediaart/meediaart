from flask import request, url_for


def build_seo(
    title=None,
    description=None,
    keywords=None,
    image=None,
):
    """
    يبني بيانات SEO الموحدة لجميع صفحات الموقع.
    """

    if image:
        image = url_for(
            "static",
            filename=f"uploads/{image}",
            _external=True,
        )
    else:
        image = url_for(
            "static",
            filename="images/logo.png",
            _external=True,
        )

    return {
        "seo_title": title,
        "seo_description": description,
        "seo_keywords": keywords,
        "seo_image": image,
        "seo_url": request.url,
    }