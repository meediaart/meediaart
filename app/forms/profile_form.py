from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional


class ProfileForm(FlaskForm):

    first_name = StringField(
        "الاسم الأول",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    last_name = StringField(
        "اسم العائلة",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    phone = StringField(
        "رقم الهاتف",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    submit = SubmitField("حفظ التعديلات")