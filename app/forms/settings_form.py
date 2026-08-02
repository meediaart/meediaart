from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, StringField, SubmitField


class SettingsForm(FlaskForm):
    site_name = StringField("اسم الموقع")
    logo = FileField("اللوجو")
    footer_text = StringField("نص الفوتر")

    submit = SubmitField("حفظ")
    show_partners = BooleanField("إظهار قسم شركاء النجاح")
    