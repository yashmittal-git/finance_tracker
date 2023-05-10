from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, BooleanField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class IncomeForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0, max=1000000)])
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    is_income = BooleanField('is_income')
