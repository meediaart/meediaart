from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class CategoryForm(FlaskForm):
    image = FileField("صورة التصنيف")

    name_ar = StringField("اسم التصنيف بالعربية", validators=[DataRequired(), Length(max=150)])
    slug_ar = StringField("الرابط المختصر بالعربية", validators=[DataRequired(), Length(max=150)])
    description_ar = TextAreaField("الوصف بالعربية", validators=[Optional()])
    keywords_ar = StringField("الكلمات المفتاحية بالعربية", validators=[Optional(), Length(max=255)])
    meta_title_ar = StringField("عنوان SEO بالعربية", validators=[Optional(), Length(max=255)])
    meta_description_ar = StringField("وصف SEO بالعربية", validators=[Optional(), Length(max=255)])

    name_en = StringField("Category name in English", validators=[Optional(), Length(max=150)])
    slug_en = StringField("English slug", validators=[Optional(), Length(max=150)])
    description_en = TextAreaField("English description", validators=[Optional()])
    keywords_en = StringField("English keywords", validators=[Optional(), Length(max=255)])
    meta_title_en = StringField("English SEO title", validators=[Optional(), Length(max=255)])
    meta_description_en = StringField("English SEO description", validators=[Optional(), Length(max=255)])

    name_ja = StringField("カテゴリー名（日本語）", validators=[Optional(), Length(max=150)])
    slug_ja = StringField("日本語スラッグ", validators=[Optional(), Length(max=150)])
    description_ja = TextAreaField("日本語説明", validators=[Optional()])
    keywords_ja = StringField("日本語キーワード", validators=[Optional(), Length(max=255)])
    meta_title_ja = StringField("日本語SEOタイトル", validators=[Optional(), Length(max=255)])
    meta_description_ja = StringField("日本語SEO説明", validators=[Optional(), Length(max=255)])

    is_active = BooleanField("تفعيل التصنيف", default=True)
    show_on_home = BooleanField("إظهار في الرئيسية", default=False)
    display_order = IntegerField("ترتيب العرض", default=0)

    submit = SubmitField("حفظ التصنيف")