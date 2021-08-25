from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Tytuł',
                           validators=[DataRequired(), Length(min=2, max=30)])
    content = TextAreaField('Treść', validators=[DataRequired()])
    picture1 = FileField('Zdjęcie 1', validators=[FileAllowed(['png', 'jpg', 'heic'])])
    picture2 = FileField('Zdjęcie 2', validators=[FileAllowed(['png', 'jpg', 'heic'])])
    picture3 = FileField('Zdjęcie 3', validators=[FileAllowed(['png', 'jpg', 'heic'])])
    submit = SubmitField('Opublikuj')

class CommentForm(FlaskForm):
    content = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Skomentuj')
