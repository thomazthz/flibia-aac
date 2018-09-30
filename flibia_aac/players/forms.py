from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class CharacterCreationForm(FlaskForm):
    name = StringField('Character name', validators=[DataRequired(), Length(min=4, max=20)])
    sex = RadioField('Sex', choices=[('0', 'Female'), ('1', 'Male')])


class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])