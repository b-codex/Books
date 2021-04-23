from flask_app.dbModels import find
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class Register(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = find("Users", "username", username)
        if (user):
            raise ValidationError(
                "Username taken. Choose a different username.")

    def validate_email(self, email):
        user = find("Users", "email", email)
        if (user):
            raise ValidationError("Email already exits.")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=16)])
    submit = SubmitField('Login')


class Comment(FlaskForm):
    text = TextAreaField('Leave Your Comment Here', validators=[DataRequired()])
    submit = SubmitField('Submit')
