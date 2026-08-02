from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class PaymentMethodForm(FlaskForm):

    payment_type = SelectField(
        "",
        choices=[
            ("card", "Card"),
            ("bank", "Bank Transfer"),
            ("paypay", "PayPay"),
            ("cash", "Cash on Delivery")
        ],
        validators=[DataRequired()]
    )

    provider = StringField(
        "",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    account_name = StringField(
        "",
        validators=[
            Optional(),
            Length(max=150)
        ]
    )

    account_number = StringField(
        "",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    is_default = BooleanField("")

    submit = SubmitField("")