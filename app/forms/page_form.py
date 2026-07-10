from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class PageForm(FlaskForm):
    title = StringField("عنوان الصفحة", validators=[DataRequired(), Length(max=150)])
    slug = StringField("الرابط (slug)", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("المحتوى", validators=[DataRequired()])
    is_active = BooleanField("نشر الصفحة")
    submit = SubmitField("حفظ الصفحة")