from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import Optional, Length


class HomeSectionForm(FlaskForm):
    # ===== العربية =====
    title_ar = StringField("العنوان بالعربية", validators=[Optional(), Length(max=200)])
    subtitle_ar = TextAreaField("النص بالعربية", validators=[Optional()])
    button_text_ar = StringField("نص الزر بالعربية", validators=[Optional(), Length(max=100)])

    # ===== الإنجليزية =====
    title_en = StringField("Title in English", validators=[Optional(), Length(max=200)])
    subtitle_en = TextAreaField("Subtitle in English", validators=[Optional()])
    button_text_en = StringField("Button text in English", validators=[Optional(), Length(max=100)])

    # ===== اليابانية =====
    title_ja = StringField("タイトル（日本語）", validators=[Optional(), Length(max=200)])
    subtitle_ja = TextAreaField("説明文（日本語）", validators=[Optional()])
    button_text_ja = StringField("ボタンテキスト（日本語）", validators=[Optional(), Length(max=100)])

    # ===== عامة =====
    button_link = StringField("رابط الزر", validators=[Optional(), Length(max=255)])
    image = FileField("رفع صورة", validators=[Optional()])

    display_order = IntegerField("الترتيب", default=0)
    is_active = BooleanField("إظهار", default=True)

    submit = SubmitField("حفظ")