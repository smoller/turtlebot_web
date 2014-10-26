#!/usr/bin/env python2

import os
import base64
import json

from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.socketio import SocketIO, emit
from flask.ext.bootstrap import Bootstrap

from forms import TourForm
from turtle_handlers import TurtleTeleOp, ImageSubscriber, MapSubscriber, PathPlanner

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='somesecretkey',
)

socketio = SocketIO(app)
bootstrap = Bootstrap(app)
mover = TurtleTeleOp()
image_sub = ImageSubscriber()
map_sub = MapSubscriber()
#path = PathPlanner()

# views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/tour/<name>')
def tour():
    tour_name = 'tour'
    tour = load_tour(tour_name)

    return render_template('tour.html', tour=tour)

@app.route('/create_tour', methods=['GET', 'POST'])
def create_tour():
    form = TourForm(request.form)
    if form.validate_on_submit():
        tour_name = form.data['name']
        save_tour(tour_name, form.data)
        flash("Tour '{}' saved.".format(tour_name))
        return redirect(url_for('create_tour'))

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

def get_tour_path(tour):
    return os.path.join(basedir, 'assets/{}.json'.format(tour))

def load_tour(tour):
    tour_path = get_tour_path(tour)
    with open(tour_path, 'r') as f:
        tour = f.read()
        return tour
    return None

def save_tour(tour, data):
    print 'Tour saved: {}'.format(tour)
    tour_path = get_tour_path(tour)
    with open(tour_path, 'wt') as f:
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
