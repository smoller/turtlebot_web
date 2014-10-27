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

    def __init__(self, tour=None, *args, **kwargs):
        super(TourForm, self).__init__(*args, **kwargs)

        if tour is not None:
            self.name.data = tour['name']
            self.waypoints.pop_entry()
            for waypoint in tour['waypoints']:
                wp_form = WaypointForm()
                wp_form.title.data = waypoint['title']
                wp_form.script.data = waypoint['script']
                self.waypoints.append_entry(wp_form)
