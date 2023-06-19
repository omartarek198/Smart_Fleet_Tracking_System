from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    id = IntegerField("ID", default=-1)
    user_type = SelectField(
        "User Type",
        validators=[DataRequired()],
        choices=["admin", "driver", "passenger"],
    )
    # user_type = StringField('User Type', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    passwd = PasswordField("Password", validators=[DataRequired()])
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
