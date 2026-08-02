from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), unique=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), nullable=False, default="customer")

    # بيانات العميل
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(30))

    # الصورة الشخصية
    avatar = db.Column(db.String(255))

    # تفعيل البريد
    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # التواريخ
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    addresses = db.relationship(
    "Address",
    back_populates="user",
    cascade="all, delete-orphan"
    )

    payment_methods = db.relationship(
        "PaymentMethod",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"