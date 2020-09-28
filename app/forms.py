
#from flask_wtf import Form
from flask_wtf import FlaskForm as Form

from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])

class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)