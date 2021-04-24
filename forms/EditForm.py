from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class UploadingForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    submit = SubmitField('Send')
