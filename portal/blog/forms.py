from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,IPAddress
from blog.models import CameraDb

class Registration(FlaskForm):
    ip=StringField('IP Address',validators=[DataRequired(),IPAddress(message="Should be ip!")])
    port=StringField('Port Number',validators=[DataRequired()])
    region=StringField('Region',validators=[DataRequired()])
    submit=SubmitField('Sign Up')
    



