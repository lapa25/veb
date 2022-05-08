from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField


class DepartmentForm(FlaskForm):
    title = StringField('Title of Department')
    chief = StringField('Chief')
    members = StringField('Members')
    email = EmailField('Email')
    submit = SubmitField('Submit')