
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    id = IntegerField('ID')
    user_type = StringField('User Type', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

