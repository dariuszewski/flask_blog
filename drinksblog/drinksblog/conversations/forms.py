from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from drinksblog.models import Message


class MessageForm(FlaskForm):
    content = TextAreaField('Wiadomość', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Wyślij')
