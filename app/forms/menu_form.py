from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    BooleanField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length, Optional


class MenuItemForm(FlaskForm):

    # ===== العربية =====
    title_ar = StringField(
        "اسم العنصر بالعربية",
        validators=[DataRequired(), Length(max=100)]
    )

    # ===== الإنجليزية =====
    title_en = StringField(
        "Menu title in English",
        validators=[Optional(), Length(max=100)]
    )

    # ===== اليابانية =====
    title_ja = StringField(
        "メニュー名（日本語）",
        validators=[Optional(), Length(max=100)]
    )

    # ===== إظهار حسب اللغة =====
    is_active_ar = BooleanField("إظهار العربية", default=True)
    is_active_en = BooleanField("Show English", default=True)
    is_active_ja = BooleanField("日本語を表示", default=True)

    # ===== نوع المحتوى =====
    content_type = SelectField(
        "نوع المحتوى",
        choices=[
            ("home", "الرئيسية"),
            ("about", "من نحن"),
            ("services", "الخدمات"),
            ("portfolio", "معرض الأعمال"),
            ("shop", "المتجر"),
            ("blog", "المدونة"),
            ("contact", "تواصل معنا"),
            ("page", "صفحة داخلية"),
            ("external", "رابط خارجي"),
        ],
        validators=[Optional()]
    )

    # ===== الصفحة المرتبطة =====
    page_id = SelectField(
        "الصفحة",
        coerce=int,
        choices=[(0, "-- اختر صفحة --")],
        validators=[Optional()]
    )

    # ===== للتوافق مع النظام الحالي =====
    endpoint = StringField(
        "Endpoint",
        validators=[Optional(), Length(max=100)]
    )

    custom_url = StringField(
        "رابط مخصص",
        validators=[Optional(), Length(max=255)]
    )

    display_order = IntegerField(
        "الترتيب",
        default=0
    )

    is_active = BooleanField(
        "نشط",
        default=True
    )

    show_on_home = BooleanField(
        "إظهار تحت السلايدر في الرئيسية",
        default=False
    )

    submit = SubmitField("حفظ عنصر القائمة")