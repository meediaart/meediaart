from flask import Blueprint, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.newsletter_subscriber import NewsletterSubscriber
from datetime import datetime


newsletter_bp = Blueprint("newsletter", __name__, url_prefix="/newsletter")


@newsletter_bp.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip()
    consent = request.form.get("consent")

    if not email:
        return {
            "success": False,
            "message": "يرجى إدخال البريد الإلكتروني"
        }

    existing = NewsletterSubscriber.query.filter_by(email=email).first()

    if existing:
        existing.is_active = True
        existing.language = session.get("lang", existing.language or "ar")

        db.session.commit()

        return {
            "success": True,
            "already_exists": True,
            "message": "أنت مشترك بالفعل في النشرة البريدية"
        }
    if not consent:
        return {
            "success": False,
            "message": "يجب الموافقة على استقبال الرسائل البريدية"
        }

    subscriber = NewsletterSubscriber(
        email=email,
        name=name if name else None,

        language=session.get("lang", "ar"),

        source="footer",

        consent_given=True,
        consent_at=datetime.utcnow(),

        ip_address=request.remote_addr
    )

    db.session.add(subscriber)
    db.session.commit()

    return {
        "success": True,
        "already_exists": False,
        "message": "تم اشتراكك في النشرة البريدية بنجاح"
    }