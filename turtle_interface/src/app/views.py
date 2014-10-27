import os
import base64
import json

from flask import render_template, request, redirect, url_for, flash

from forms import TourForm
from . import app, socketio, teleop, map_sub, image_sub
from config import basedir

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

@app.route('/manage_tours', methods=['GET', 'POST'])
@app.route('/manage_tours/', methods=['GET', 'POST'])
def manage_tours():
    tours = get_tour_list()
    form = TourForm()

    tour_name = request.form.get('select_tour')
    if tour_name is not None and tour_name != '':
            tour_data = load_tour(tour_name)
            form = TourForm(tour=tour_data)
            flash("Tour '{}' loaded.".format(tour_name))
    if form.validate_on_submit():
        tour_name = form.data['name']
        save_tour(tour_name, form.data)
        flash("Tour '{}' saved.".format(tour_name))
        return redirect(url_for('manage_tours'))

    return render_template('manage_tours.html', 
            form=form,
            tours=tours)

# Socket events
@socketio.on('move', namespace='/move')
def move(data):
    print(data['x'], data['y'])
    teleop.move(data['x'], data['y'])

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

@socketio.on('move to waypoint', namespace='/waypoint')
def map_move(waypoint):
    #TODO Move robot here
    #teleop.moveToWaypoint(waypoint['position'], waypoint['id'])
    emit('move complete', waypoint)

# utilities
def image_to_json(img):
    return {'value': 'data:image/png;base64,'+base64.encodestring(img)}

def get_tour_path(tour):
    return os.path.join(basedir, 'assets/tours/{}.json'.format(tour))

def load_tour(tour):
    tour_path = get_tour_path(tour)
    with open(tour_path, 'r') as f:
        return json.load(f)
    return None

def save_tour(tour, data):
    print 'Tour saved: {}'.format(tour)
    tour_path = get_tour_path(tour)
    with open(tour_path, 'wt') as f:
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

def get_tour_list():
    tour_path = os.path.join(basedir, 'assets/tours/')
    return [name for name, ext in map(os.path.splitext, os.listdir(tour_path)) if ext == '.json']
