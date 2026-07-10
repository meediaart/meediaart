from flask import Blueprint, render_template
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
    post = Post.query.filter(
        or_(
            Post.slug == slug,
            Post.slug_ar == slug,
            Post.slug_en == slug,
            Post.slug_ja == slug
        ),
        Post.is_active == True
    ).first()

    if not post:
        return render_template("blog/article.html", post=None), 404

    return render_template(
        "blog/article.html",
        post=post
    )