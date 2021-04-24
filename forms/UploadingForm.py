from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import DataRequired


class UploadingForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    file = FileField('Файл', validators=[DataRequired()])
    submit = SubmitField('Send')
