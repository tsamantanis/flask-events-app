from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField
)
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

class SignUpForm(FlaskForm):
    """Form for adding a Users."""
    username = StringField('Username',
        validators=[DataRequired(), Length(min = 3, max = 50)])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for logging Users in."""
    username = StringField('Username',
        validators = [DataRequired(), Length(min = 3, max = 80)])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log In')