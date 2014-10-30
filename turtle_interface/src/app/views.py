import base64
import json

from flask import render_template, request, redirect, url_for, flash
from flask.ext.socketio import emit
from forms import TourForm
from . import app, socketio, teleop, map_sub, image_sub
from config import basedir
from models import Tour, get_tour_list 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/tour/<name>')
def tour(name):
    
    tour = Tour(name)
    return render_template('tour.html', tour=json.dumps(tour.load_tour()))

@app.route('/manage_tours', methods=['GET', 'POST'])
def manage_tours():
    tours = get_tour_list()
    selected_tour = None
    form = TourForm()

    tour_name = request.form.get('select_tour')
    if tour_name is not None and tour_name != '':
            tour_data = Tour(tour_name).load_tour()
            form = TourForm(tour=tour_data)
            flash("Tour '{}' loaded.".format(tour_name))
            selected_tour = tour_name
    if form.validate_on_submit():
        tour_name = form.data['name']
        Tour(tour_name).save_tour(form.data)
        flash("Tour '{}' saved.".format(tour_name))
        return redirect(url_for('manage_tours'))

    return render_template('manage_tours.html', 
            form=form,
            tours=tours,
            selected_tour=selected_tour)

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

@socketio.on('move_to_waypoint', namespace='/waypoint')
def map_move(waypoint):
    #TODO Move robot here
    teleop.moveToWaypoint(waypoint['position'], waypoint['id'])
    emit('move_complete', waypoint)

# utilities
def image_to_json(img):
    return {'value': 'data:image/png;base64,'+base64.encodestring(img)}


