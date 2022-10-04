from flask_wtf import FlaskForm
from pyparsing import Regex
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, EmailField, validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from app.models.users import User


class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirmer mot de passe ', validators=[
        DataRequired(),
        EqualTo('password', message='mot de passe différent'),
        Length(min=8, max=20)
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
