from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import roslib
roslib.load_manifest('turtlebot_web')
from turtle_telop import TurtleTeleOp

socketio = SocketIO(app)
mover = TurtleTeleOp()

app = Flask(__name__)

app.config.update(
    DEBUG=True,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move')
def move_page():
    return render_template('move.html')

@socketio.on('move', namespace='/drive')
def move(data):
    mover.move(data['x'], data['y'])

if __name__ == '__main__':
    socketio.run(app)
