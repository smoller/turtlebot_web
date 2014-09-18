from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from roslib
roslib.load_manifest('turtlebot_web')
from turtle_telop import TurtleTeleOp

app = Flask(__name__)
socketio = SocketIO(app)

app.config.update(
    DEBUG=True,
)

mover = TurtleTeleOp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move')
def move_page():
    return render_template('move.html')

@socketio.on('move', namespace='/test') 
def move(message):
    mover.move(message['x'], message['y'])

if __name__ == '__main__':
    socketio.run(app)
