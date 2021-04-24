from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import DataRequired


class RandimpForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    submit = SubmitField('Send')
