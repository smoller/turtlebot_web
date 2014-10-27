from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.socketio import SocketIO

from turtle_handlers import TurtleTeleOp, ImageSubscriber, MapSubscriber, PathPlanner

app = Flask(__name__)
app.config.from_object('config')

socketio = SocketIO(app)
bootstrap = Bootstrap(app)

teleop = TurtleTeleOp()
image_sub = ImageSubscriber()
map_sub = MapSubscriber()

from app import views
