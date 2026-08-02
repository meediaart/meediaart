from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):

    # ===== العربية =====
    title_ar = StringField("عنوان المقال بالعربية", validators=[DataRequired(), Length(max=200)])
    slug_ar = StringField("الرابط المختصر بالعربية", validators=[DataRequired(), Length(max=200)])

    excerpt_ar = StringField("نبذة مختصرة بالعربية", validators=[Optional(), Length(max=255)])
    content_ar = TextAreaField("المحتوى بالعربية", validators=[Optional()])

    keywords_ar = StringField("الكلمات المفتاحية بالعربية", validators=[Optional(), Length(max=255)])
    meta_title_ar = StringField("عنوان SEO بالعربية", validators=[Optional(), Length(max=255)])
    meta_description_ar = StringField("وصف SEO بالعربية", validators=[Optional(), Length(max=255)])

    # ===== الإنجليزية =====
    title_en = StringField("Post title in English", validators=[Optional(), Length(max=200)])
    slug_en = StringField("Slug in English", validators=[Optional(), Length(max=200)])

    excerpt_en = StringField("Short excerpt in English", validators=[Optional(), Length(max=255)])
    content_en = TextAreaField("Content in English", validators=[Optional()])

    keywords_en = StringField("Keywords in English", validators=[Optional(), Length(max=255)])
    meta_title_en = StringField("SEO Title in English", validators=[Optional(), Length(max=255)])
    meta_description_en = StringField("SEO Description in English", validators=[Optional(), Length(max=255)])

    # ===== اليابانية =====
    title_ja = StringField("記事タイトル（日本語）", validators=[Optional(), Length(max=200)])
    slug_ja = StringField("スラッグ（日本語）", validators=[Optional(), Length(max=200)])

    excerpt_ja = StringField("短い説明（日本語）", validators=[Optional(), Length(max=255)])
    content_ja = TextAreaField("本文（日本語）", validators=[Optional()])

    keywords_ja = StringField("キーワード（日本語）", validators=[Optional(), Length(max=255)])
    meta_title_ja = StringField("SEOタイトル（日本語）", validators=[Optional(), Length(max=255)])
    meta_description_ja = StringField("SEO説明（日本語）", validators=[Optional(), Length(max=255)])

    # ===== عامة =====
    image = FileField("الصورة التعبيرية", validators=[Optional()])

    is_active = BooleanField("منشور", default=True)
    show_on_home = BooleanField("إظهار في الرئيسية", default=False)

    submit = SubmitField("حفظ المقال")