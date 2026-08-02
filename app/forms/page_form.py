from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class PageForm(FlaskForm):

    # ========= العناوين =========
    title_ar = StringField(
        "العنوان (العربية)",
        validators=[DataRequired(), Length(max=150)]
    )

    title_en = StringField(
        "Title (English)",
        validators=[Optional(), Length(max=150)]
    )

    title_ja = StringField(
        "タイトル（日本語）",
        validators=[Optional(), Length(max=150)]
    )

    # ========= الروابط =========
    slug_ar = StringField(
        "Slug (AR)",
        validators=[DataRequired(), Length(max=150)]
    )

    slug_en = StringField(
        "Slug (EN)",
        validators=[Optional(), Length(max=150)]
    )

    slug_ja = StringField(
        "Slug (JA)",
        validators=[Optional(), Length(max=150)]
    )

    # ========= المحتوى =========
    content = TextAreaField(
        "المحتوى",
        validators=[Optional()]
    )
    
    content_ar = TextAreaField("المحتوى (العربية)")
    content_en = TextAreaField("Content (English)")
    content_ja = TextAreaField("コンテンツ（日本語）")

    # ========= إعدادات الصفحة =========
    page_type = SelectField(
        "نوع الصفحة",
        choices=[
            ("main", "صفحة رئيسية"),
            ("child", "صفحة فرعية")
        ],
        default="main"
    )
    
    parent_id = SelectField(
    "الصفحة الأم",
    coerce=int,
    validators=[Optional()],
    choices=[(0, "— لا يوجد —")]
    )

    template = SelectField(
        "قالب الصفحة",
        choices=[
            ("default", "صفحة عادية"),
            ("services", "الخدمات"),
            ("portfolio", "الأعمال"),
            ("shop", "المتجر"),
            ("blog", "المدونة"),
            ("contact", "اتصل بنا")
        ],
        default="default"
    )

    display_order = IntegerField(
        "ترتيب الظهور",
        default=0
    )

    # ========= أماكن الظهور =========
    show_in_menu = BooleanField(
        "إظهار في القائمة الرئيسية",
        default=True
    )

    show_on_home = BooleanField(
        "إظهار في الصفحة الرئيسية"
    )

    show_in_footer = BooleanField(
        "إظهار في Footer"
    )

    is_active = BooleanField(
        "الصفحة مفعلة",
        default=True
    )

    submit = SubmitField("حفظ الصفحة")