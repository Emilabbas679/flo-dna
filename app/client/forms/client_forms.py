from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField, SelectField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo
from wtforms import validators
from wtforms.validators import Length
from wtforms.fields.html5 import EmailField
from flask_babelex import _


class OrderForm(FlaskForm):
    address = StringField(_('Pickup location'),
                                  render_kw={'placeholder': 'Pickup location'},
                                  validators=[DataRequired()]
                                  )
    receiver_name = StringField(_('Receiver name'))
    receiver_phone = StringField(_('Receiver phone'))
    message = StringField(_('Message'), validators=[DataRequired()])
    payment_type = StringField(_('Payment type'))
    total_price = FloatField(_('Total price'))
    delivery_type = StringField(_('Delivery type'))
    pickup_lng = HiddenField()
    pickup_ltd = HiddenField()

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email address', [validators.DataRequired(), validators.Email()])
    name = StringField('name', validators=[DataRequired()])
    # lastName = StringField('lastName', validators=[DataRequired()])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class UpdateUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    lastName = StringField('lastName', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', [InputRequired()])
    new_password = PasswordField('New Password', [EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')


class VerifyForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])


class AccountForm(FlaskForm):
    pass


class CountryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    code = StringField('code', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])
