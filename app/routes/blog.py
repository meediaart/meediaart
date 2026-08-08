from flask import (
    Blueprint,
    render_template,
    session,
    url_for,
)
from sqlalchemy import or_

from app.models.post import Post

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


@blog_bp.route("/")
def index():
    posts = Post.query.filter_by(is_active=True).order_by(Post.id.desc()).all()

    return render_template(
        "blog/index.html",
        posts=posts
    )


@blog_bp.route("/<slug>")
def article(slug):

    current_lang = session.get("lang", "ar")

    post = Post.query.filter(
        or_(
            Post.slug == slug,
            Post.slug_ar == slug,
            Post.slug_en == slug,
            Post.slug_ja == slug
        ),
        Post.is_active == True
    ).first_or_404()

    # =========================
    # SEO الخاص بالمقال
    # =========================

    seo_title = post.get_meta_title(current_lang)

    seo_description = (
        post.get_meta_description(current_lang)
        or post.get_excerpt(current_lang)
        or ""
    )

    seo_keywords = (
        post.get_keywords(current_lang)
        or ""
    )

    if post.image:
        seo_image = url_for(
            "static",
            filename="uploads/" + post.image,
            _external=True,
        )
    else:
        seo_image = url_for(
            "static",
            filename="images/logo.png",
            _external=True,
        )

    seo_url = url_for(
        "blog.article",
        slug=post.get_slug(current_lang),
        _external=True,
    )

    return render_template(
        "blog/article.html",
        post=post,
        current_lang=current_lang,

        # SEO
        seo_title=seo_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords,
        seo_image=seo_image,
        seo_url=seo_url,

        # المقالات يفضل أن تكون article في Open Graph
        seo_og_type="article",
    )