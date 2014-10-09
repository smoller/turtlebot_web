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

# views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('demo')
def demo():
    return render_template('demo.html')


# Socket events
@socketio.on('move', namespace='/move')
def move(data):
    mover.move(data['x'], data['y'])

@socketio.on('map', namespace='/map') 
def map(): 
    """
    map = mapper.map()
    json_map = json(map)
    emit('new map', json_map)
    """
    pass

@socketio.on('photo', namespace='/photo')
def photo():
    """
    photo = photo.map()
    json_photo = json(photo)
    emit('new photo', json_photo)
    """
    pass



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
