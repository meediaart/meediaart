from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class TeamMemberForm(FlaskForm):

    # =========================
    # العربية
    # =========================
    name_ar = StringField(
        "الاسم بالعربي",
        validators=[DataRequired(), Length(max=150)]
    )

    slug_ar = StringField(
        "الرابط بالعربي",
        validators=[DataRequired(), Length(max=150)]
    )

    job_title_ar = StringField(
        "المنصب بالعربي",
        validators=[Optional(), Length(max=150)]
    )

    short_bio_ar = TextAreaField(
        "نبذة قصيرة بالعربي",
        validators=[Optional()]
    )

    full_bio_ar = TextAreaField(
        "السيرة الذاتية بالعربي",
        validators=[Optional()]
    )

    # =========================
    # الإنجليزية
    # =========================
    name_en = StringField(
        "الاسم بالإنجليزية",
        validators=[Optional(), Length(max=150)]
    )

    slug_en = StringField(
        "الرابط بالإنجليزية",
        validators=[Optional(), Length(max=150)]
    )

    job_title_en = StringField(
        "المنصب بالإنجليزية",
        validators=[Optional(), Length(max=150)]
    )

    short_bio_en = TextAreaField(
        "نبذة قصيرة بالإنجليزية",
        validators=[Optional()]
    )

    full_bio_en = TextAreaField(
        "السيرة الذاتية بالإنجليزية",
        validators=[Optional()]
    )

    # =========================
    # اليابانية
    # =========================
    name_ja = StringField(
        "الاسم باليابانية",
        validators=[Optional(), Length(max=150)]
    )

    slug_ja = StringField(
        "الرابط باليابانية",
        validators=[Optional(), Length(max=150)]
    )

    job_title_ja = StringField(
        "المنصب باليابانية",
        validators=[Optional(), Length(max=150)]
    )

    short_bio_ja = TextAreaField(
        "نبذة قصيرة باليابانية",
        validators=[Optional()]
    )

    full_bio_ja = TextAreaField(
        "السيرة الذاتية باليابانية",
        validators=[Optional()]
    )

    # =========================
    # بيانات عامة
    # =========================
    image = FileField(
        "صورة العضو",
        validators=[Optional()]
    )

    display_order = IntegerField(
        "الترتيب",
        default=0
    )

    is_active = BooleanField(
        "إظهار العضو",
        default=True
    )

    show_on_home = BooleanField(
        "إظهار في الرئيسية",
        default=False
    )

    submit = SubmitField("حفظ")