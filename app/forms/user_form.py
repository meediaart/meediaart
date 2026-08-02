from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email

from app.models.user import User


class UserForm(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired()])
    email = StringField("البريد الإلكتروني", validators=[DataRequired(), Email()])
    password = PasswordField("كلمة المرور", validators=[DataRequired()])
    role = SelectField(
        "الدور",
        choices=[("admin", "admin"), ("editor", "editor")],
        validators=[DataRequired()]
    )
    submit = SubmitField("حفظ المستخدم")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("اسم المستخدم مستخدم مسبقًا")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("البريد الإلكتروني مستخدم مسبقًا")