from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class AddressForm(FlaskForm):

    full_name = StringField(
        "الاسم الكامل",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    phone = StringField(
        "رقم الهاتف",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    postal_code = StringField(
        "الرمز البريدي",
        validators=[
            Optional(),
            Length(max=20)
        ]
    )

    prefecture = StringField(
        "المحافظة",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    city = StringField(
        "المدينة",
        validators=[
            Optional(),
            Length(max=150)
        ]
    )

    address_line = StringField(
        "العنوان",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    building = StringField(
        "المبنى / الشقة",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    is_default = BooleanField(
        "تعيين كعنوان افتراضي"
    )

    submit = SubmitField("حفظ العنوان")