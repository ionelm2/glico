from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields import DateField
from datetime import datetime
import sqlalchemy as sa
from app import db
from app.models import User, Bond

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BondForm(FlaskForm):
    # TODO: change in template with <select ...> to allowe selecting the type
    type = StringField('Tip', validators=[DataRequired()])
    ticker = StringField('Cod Emisiune', validators=[DataRequired()])
    currency = StringField('Valuta', validators=[DataRequired()])
    broker = StringField('Broker', validators=[DataRequired()])
    period = StringField('Perioada', validators=[DataRequired()])
    #enddate = StringField('Scadenta', validators=[DataRequired()])
    #enddate = DateField('End Date',default=date.today())
    enddate = DateField('End Date',default=datetime.now().date())
    interest = StringField('Dobanda', validators=[DataRequired()])
    
    #submit = SubmitField('Salveaza')

class BondTransactionForm(FlaskForm):
    def validate_ticker(self, ticker):
        tick = db.session.scalar(sa.select(Bond).where(
            Bond.ticker == ticker.data))
        if tick is None:
            raise ValidationError('Please use a different username.')
        
    ticker = StringField('Cod Emisiune', validators=[DataRequired(),validate_ticker])
    date = StringField('Data', default=datetime.now().date())
    operation = StringField('Operatie', validators=[DataRequired()])
    amount = StringField('Valoare', validators=[DataRequired()])

    submit = SubmitField('Adauga')

    