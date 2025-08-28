from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Passwords must match.')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=100)])
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    skill_type = SelectField(
        "Type",
        choices=[('offer','I can offer'),('learn', 'I want to learn')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Save')