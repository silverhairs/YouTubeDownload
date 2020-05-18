from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    video_url = StringField('Paste the YouTube URL here', validators=[DataRequired()])
    search = SubmitField('Search')