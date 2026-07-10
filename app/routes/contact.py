from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app.extensions import db
from app.models.contact_message import ContactMessage
from app.models.newsletter_subscriber import NewsletterSubscriber


contact_bp = Blueprint("contact", __name__, url_prefix="/contact")


@contact_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("يرجى تعبئة الاسم والبريد والرسالة", "error")
            return redirect(url_for("contact.index"))

        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        db.session.add(contact_message)

        existing_subscriber = NewsletterSubscriber.query.filter_by(
            email=email
        ).first()

        if not existing_subscriber:
            subscriber = NewsletterSubscriber(
                email=email,
                name=name,
                language=session.get("lang", "ar"),
                source="contact_page"
            )

            db.session.add(subscriber)

        db.session.commit()

        flash("تم إرسال رسالتك بنجاح، سنتواصل معك قريبًا", "success")
        return redirect(url_for("contact.index"))

    return render_template("contact/index.html")