from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField


class JobForm(FlaskForm):
    job = StringField('Job title')
    team_leader = IntegerField('Team leader id')
    work_size = IntegerField('Work size')
    collaborators = StringField('Collaborators')
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')
