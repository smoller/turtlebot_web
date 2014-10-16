#!/usr/bin/env python2

import base64

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from turtle_handlers.turtle_teleop import TurtleTeleOp
from turtle_handlers.image_subscriber import ImageSubscriber
from turtle_handlers.map_subscriber import MapSubscriber

app = Flask(__name__)

socketio = SocketIO(app)
mover = TurtleTeleOp()
image_sub = ImageSubscriber()
map_sub = MapSubscriber()

app.config.update(
    DEBUG=True,
)

# views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')


# Socket events
@socketio.on('move', namespace='/move')
def move(data):
    print (data['x'], data['y'])
    mover.move(data['x'], data['y'])

@socketio.on('map', namespace='/map') 
def map_image(): 
    map_image = map_sub.get_map_image()
    if map_image is not None:
        emit('new map', image_to_json(map_image))

@socketio.on('photo', namespace='/photo')
def photo():
    photo = image_sub.photo()
    if photo is not None:
        emit('new photo', image_to_json(photo))

def image_to_json(img):
    return {'value':'data:image/png;base64,'+base64.encodestring(img)}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
