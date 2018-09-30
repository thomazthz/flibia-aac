from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from ..db import db

from .models import Account


class RegistrationForm(FlaskForm):
    name = StringField('Account name', validators=[DataRequired(), Length(min=6, max=32)])
    email = StringField('Email', validators=[Length(min=6, max=35)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=8, max=30),
    ])
    confirm = PasswordField('Password again')

    def validate_name(self, field):
        if db.session.query(db.func.count(Account.id)).filter_by(name=field.data).scalar():
            raise ValidationError('This "Account name" is already taken')


class LoginForm(FlaskForm):
    name = StringField('Account name:', validators=[DataRequired(), Length(min=6, max=32)])
    password = PasswordField('Password:', validators=[DataRequired()])
