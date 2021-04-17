from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_app.models import User
from flask_app import db


class Register(FlaskForm):
    db.create_all()
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if (user):
            raise ValidationError(
                "Username taken. Choose a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if (user):
            raise ValidationError("Email already exits.")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=16)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
