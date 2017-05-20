from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username:',
                           validators=[
                               DataRequired(), Length(3,80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, '
                                              'letters and underscores.')])

    password = PasswordField('Password:',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2',
                                         message='Passwords must match.')
                             ])

    password2 = PasswordField('Confirm Password:',validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_username(self, extra):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('This username is already taken.')
