from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class ServiceForm(FlaskForm):
    # ===== العربية =====
    title_ar = StringField("عنوان الخدمة بالعربية", validators=[DataRequired(), Length(max=200)])
    slug_ar = StringField("الرابط المختصر بالعربية", validators=[DataRequired(), Length(max=200)])
    short_description_ar = StringField("وصف مختصر بالعربية", validators=[Optional(), Length(max=255)])
    description_ar = TextAreaField("الوصف الكامل بالعربية", validators=[Optional()])
    keywords_ar = StringField("الكلمات المفتاحية بالعربية", validators=[Optional(), Length(max=255)])
    meta_title_ar = StringField("عنوان SEO بالعربية", validators=[Optional(), Length(max=255)])
    meta_description_ar = StringField("وصف SEO بالعربية", validators=[Optional(), Length(max=255)])
    is_active_ar = BooleanField("إظهار العربية", default=True)

    # ===== الإنجليزية =====
    title_en = StringField("Title in English", validators=[Optional(), Length(max=200)])
    slug_en = StringField("Slug in English", validators=[Optional(), Length(max=200)])
    short_description_en = StringField("Short description in English", validators=[Optional(), Length(max=255)])
    description_en = TextAreaField("Full description in English", validators=[Optional()])
    keywords_en = StringField("Keywords in English", validators=[Optional(), Length(max=255)])
    meta_title_en = StringField("SEO Title in English", validators=[Optional(), Length(max=255)])
    meta_description_en = StringField("SEO Description in English", validators=[Optional(), Length(max=255)])
    is_active_en = BooleanField("Show English", default=True)

    # ===== اليابانية =====
    title_ja = StringField("サービス名（日本語）", validators=[Optional(), Length(max=200)])
    slug_ja = StringField("スラッグ（日本語）", validators=[Optional(), Length(max=200)])
    short_description_ja = StringField("短い説明（日本語）", validators=[Optional(), Length(max=255)])
    description_ja = TextAreaField("詳しい説明（日本語）", validators=[Optional()])
    keywords_ja = StringField("キーワード（日本語）", validators=[Optional(), Length(max=255)])
    meta_title_ja = StringField("SEOタイトル（日本語）", validators=[Optional(), Length(max=255)])
    meta_description_ja = StringField("SEO説明（日本語）", validators=[Optional(), Length(max=255)])
    is_active_ja = BooleanField("日本語を表示", default=True)

    # ===== عامة =====
    image = FileField("الصورة الرئيسية")

    images = MultipleFileField("صور إضافية للمنتج")
    icon = StringField("الأيقونة", validators=[Optional(), Length(max=100)])
    booking_link = StringField("رابط الحجز أو الاستشارة", validators=[Optional(), Length(max=255)])

    display_order = IntegerField("الترتيب", default=0)
    is_active = BooleanField("منشور", default=True)
    show_on_home = BooleanField("إظهار في الصفحة الرئيسية", default=False)

    submit = SubmitField("حفظ الخدمة")