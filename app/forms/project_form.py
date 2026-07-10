from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired, Length, Optional


class ProjectForm(FlaskForm):
    title = StringField("عنوان المشروع", validators=[DataRequired(), Length(max=200)])
    slug = StringField("الرابط المختصر", validators=[DataRequired(), Length(max=200)])

    short_description = StringField("وصف مختصر", validators=[Optional(), Length(max=255)])
    description = TextAreaField("الوصف الكامل", validators=[Optional()])

    image = FileField("الصورة الرئيسية")

    images = MultipleFileField("صور إضافية للمنتج")

    client_name = StringField("اسم العميل", validators=[Optional(), Length(max=150)])
    project_type = StringField("نوع المشروع", validators=[Optional(), Length(max=150)])

    keywords = StringField("الكلمات المفتاحية", validators=[Optional(), Length(max=255)])
    meta_title = StringField("عنوان SEO", validators=[Optional(), Length(max=255)])
    meta_description = StringField("وصف SEO", validators=[Optional(), Length(max=255)])

    display_order = IntegerField("الترتيب", default=0)
    is_active = BooleanField("منشور", default=True)
    show_on_home = BooleanField("إظهار في الصفحة الرئيسية")

    submit = SubmitField("حفظ المشروع")