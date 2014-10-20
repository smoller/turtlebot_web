from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class TourForm(Form):
    name = TextField('Tour name', validators=[Required()])
