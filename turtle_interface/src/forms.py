from flask.ext.wtf import Form
from wtforms import TextField, FormField, FieldList, SubmitField
from wtforms.validators import Required

class WaypointForm(Form):
    title = TextField('Name', validators=[Required()])
    script = TextField('Script')

class TourForm(Form):
    name = TextField('Name', validators=[Required()])
    waypoints = FieldList(FormField(WaypointForm), min_entries=3)
    submit = SubmitField("Submit")
