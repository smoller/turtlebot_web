#!/usr/bin/env python2

import base64
import json

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from forms import TourForm

from turtle_handlers import TurtleTeleOp, ImageSubscriber, MapSubscriber

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='somesecretkey',
)

socketio = SocketIO(app)
mover = TurtleTeleOp()
image_sub = ImageSubscriber()
map_sub = MapSubscriber()

# views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/tour')
def tour():
    tour = {}
    tour_name = 'tour'
    tour_path = 'assets/{}.json'.format(tour_name)
    with open(tour_path, 'r') as f:
        tour = f.read()

    return render_template('tour.html', tour=tour)

@app.route('/create_tour', methods=['GET', 'POST'])
def create_tour():
    form = TourForm()
    if form.validate_on_submit():
        print form.name.data

    return render_template('create_tour.html', form=form)

# Socket events
@socketio.on('move', namespace='/move')
def move(data):
    print(data['x'], data['y'])
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

# utilities
def image_to_json(img):
    return {'value': 'data:image/png;base64,'+base64.encodestring(img)}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
