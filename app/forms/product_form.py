from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import (
    BooleanField,
    DecimalField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductForm(FlaskForm):
    # ===== العربية =====
    title_ar = StringField("اسم المنتج بالعربية", validators=[DataRequired(), Length(max=200)])
    slug_ar = StringField("الرابط المختصر بالعربية", validators=[DataRequired(), Length(max=200)])
    description_ar = TextAreaField("الوصف بالعربية", validators=[Optional()])
    keywords_ar = StringField("الكلمات المفتاحية بالعربية", validators=[Optional(), Length(max=255)])
    meta_title_ar = StringField("عنوان SEO بالعربية", validators=[Optional(), Length(max=255)])
    meta_description_ar = StringField("وصف SEO بالعربية", validators=[Optional(), Length(max=255)])
    is_active_ar = BooleanField("إظهار العربية", default=True)

    # ===== الإنجليزية =====
    title_en = StringField("Product title in English", validators=[Optional(), Length(max=200)])
    slug_en = StringField("Slug in English", validators=[Optional(), Length(max=200)])
    description_en = TextAreaField("Description in English", validators=[Optional()])
    keywords_en = StringField("Keywords in English", validators=[Optional(), Length(max=255)])
    meta_title_en = StringField("SEO Title in English", validators=[Optional(), Length(max=255)])
    meta_description_en = StringField("SEO Description in English", validators=[Optional(), Length(max=255)])
    is_active_en = BooleanField("Show English", default=True)

    # ===== اليابانية =====
    title_ja = StringField("商品名（日本語）", validators=[Optional(), Length(max=200)])
    slug_ja = StringField("スラッグ（日本語）", validators=[Optional(), Length(max=200)])
    description_ja = TextAreaField("説明（日本語）", validators=[Optional()])
    keywords_ja = StringField("キーワード（日本語）", validators=[Optional(), Length(max=255)])
    meta_title_ja = StringField("SEOタイトル（日本語）", validators=[Optional(), Length(max=255)])
    meta_description_ja = StringField("SEO説明（日本語）", validators=[Optional(), Length(max=255)])
    is_active_ja = BooleanField("日本語を表示", default=True)

    # ===== عامة =====
    price = DecimalField("السعر", validators=[DataRequired(), NumberRange(min=0)])
    discount_percent = FloatField("نسبة الخصم", default=0, validators=[Optional(), NumberRange(min=0, max=100)])

    image = FileField("الصورة الرئيسية")
    images = MultipleFileField("صور إضافية للمنتج")

    category_id = SelectField("التصنيف", coerce=int, validators=[DataRequired()])
    display_order = IntegerField("الترتيب", default=0, validators=[Optional()])

    is_active = BooleanField("نشر المنتج", default=True)
    show_on_home = BooleanField("إظهار في الرئيسية", default=False)

    # ===== خيارات المنتج =====
    has_colors = BooleanField("يوجد ألوان", default=False)
    available_colors = StringField("الألوان المتوفرة", validators=[Optional(), Length(max=255)])

    has_sizes = BooleanField("يوجد مقاسات", default=False)
    available_sizes = StringField("المقاسات المتوفرة", validators=[Optional(), Length(max=255)])

    # ===== التخصيص =====
    allow_custom_text = BooleanField("السماح بنص مخصص", default=False)
    allow_custom_image = BooleanField("السماح برفع صورة مخصصة", default=False)

        # ===== التقييمات والتعليقات =====
    ratings_enabled = BooleanField(
        "تفعيل تقييم النجوم",
        default=True
    )

    comments_enabled = BooleanField(
        "تفعيل التعليقات والصور",
        default=True
    )

    submit = SubmitField("حفظ المنتج")