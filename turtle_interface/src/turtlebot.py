#!/bin/env python2
import base64
import cv2

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
        base64_map = base64.encodestring(map_image)
        json_map = { 'value':base64_map }
        emit('new map', json_map)

@socketio.on('photo', namespace='/photo')
def photo():
    photo = image_sub.photo()
    if photo is not None:
        base64_photo = base64.encodestring(photo)
        json_photo = { 'value':base64_photo }
        emit('new photo', json_photo)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
