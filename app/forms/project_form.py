from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import (
    BooleanField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class ProjectForm(FlaskForm):

    # ========= العربية =========
    title_ar = StringField(
        "العنوان (عربي)",
        validators=[DataRequired(), Length(max=200)],
    )

    slug_ar = StringField(
        "الرابط (عربي)",
        validators=[DataRequired(), Length(max=200)],
    )

    short_description_ar = StringField(
        "وصف مختصر (عربي)",
        validators=[Optional(), Length(max=255)],
    )

    description_ar = TextAreaField(
        "الوصف (عربي)",
        validators=[Optional()],
    )

    keywords_ar = StringField(
        "الكلمات المفتاحية (عربي)",
        validators=[Optional(), Length(max=255)],
    )

    meta_title_ar = StringField(
        "عنوان SEO (عربي)",
        validators=[Optional(), Length(max=255)],
    )

    meta_description_ar = StringField(
        "وصف SEO (عربي)",
        validators=[Optional(), Length(max=255)],
    )

    # ========= الإنجليزية =========

    title_en = StringField(
        "Title (English)",
        validators=[Optional(), Length(max=200)],
    )

    slug_en = StringField(
        "Slug (English)",
        validators=[Optional(), Length(max=200)],
    )

    short_description_en = StringField(
        "Short Description (English)",
        validators=[Optional(), Length(max=255)],
    )

    description_en = TextAreaField(
        "Description (English)",
        validators=[Optional()],
    )

    keywords_en = StringField(
        "Keywords (English)",
        validators=[Optional(), Length(max=255)],
    )

    meta_title_en = StringField(
        "SEO Title (English)",
        validators=[Optional(), Length(max=255)],
    )

    meta_description_en = StringField(
        "SEO Description (English)",
        validators=[Optional(), Length(max=255)],
    )

    # ========= اليابانية =========

    title_ja = StringField(
        "タイトル",
        validators=[Optional(), Length(max=200)],
    )

    slug_ja = StringField(
        "スラッグ",
        validators=[Optional(), Length(max=200)],
    )

    short_description_ja = StringField(
        "概要",
        validators=[Optional(), Length(max=255)],
    )

    description_ja = TextAreaField(
        "説明",
        validators=[Optional()],
    )

    keywords_ja = StringField(
        "キーワード",
        validators=[Optional(), Length(max=255)],
    )

    meta_title_ja = StringField(
        "SEOタイトル",
        validators=[Optional(), Length(max=255)],
    )

    meta_description_ja = StringField(
        "SEO説明",
        validators=[Optional(), Length(max=255)],
    )

    # ========= عامة =========

    image = FileField("الصورة الرئيسية")

    images = MultipleFileField("صور إضافية")

    client_name = StringField(
        "اسم العميل",
        validators=[Optional(), Length(max=150)],
    )

    project_type = StringField(
        "نوع المشروع",
        validators=[Optional(), Length(max=150)],
    )

    display_order = IntegerField(
        "الترتيب",
        default=0,
    )

    is_active = BooleanField(
        "منشور",
        default=True,
    )

    show_on_home = BooleanField(
        "إظهار في الصفحة الرئيسية",
    )

    submit = SubmitField("حفظ المشروع")