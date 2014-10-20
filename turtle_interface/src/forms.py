from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class TourForm(Form):
    name = TextField('Name', validators=[Required()])

class WaypointForm(Form):
    name = TextField('Name', validators=[Required()])
    script = TextField('Script')
