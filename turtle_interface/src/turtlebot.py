#!/usr/bin/env python2

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from turtle_handlers.turtle_teleop import TurtleTeleOp

app = Flask(__name__)

socketio = SocketIO(app)
mover = TurtleTeleOp()

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
<<<<<<< Updated upstream
    print(data['x'], data['y'])
=======
    print 'moving now?'
>>>>>>> Stashed changes
    mover.move(data['x'], data['y'])

if __name__ == '__main__':
    socketio.run(app)
