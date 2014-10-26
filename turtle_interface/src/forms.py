from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, FormField, FieldList
from wtforms.validators import Required

class WaypointForm(Form):
    title = TextField('Name', validators=[Required()])
    script = TextAreaField('Script')
    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(csrf_enabled=False, *args, **kwargs)

class TourForm(Form):
    name = TextField('Name', validators=[Required()])
    waypoints = FieldList(FormField(WaypointForm), min_entries=1)
