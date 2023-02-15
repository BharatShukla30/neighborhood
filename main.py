import sqlite3

from math import radians, sin, cos, sqrt, atan2
from constants import ARCGIS_URL, ARCGIS_API_KEY
from model.User import db, Users
from flask import Flask, request, render_template, jsonify
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode

gis = GIS(ARCGIS_URL, api_key = ARCGIS_API_KEY)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


def location_formatting(address):
    """
    This function changes the text location into geographical coordinates
    Note: arcgis api returns coordinates in format x:longitude, y:latitude
    """
    geocoded_adr = geocode(address)
    latitude = geocoded_adr[0]['location']['y']
    longitude = geocoded_adr[0]['location']['x']
    return '{}, {}'.format(latitude, longitude)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        blood_group = request.form['blood_group']
        user_type = request.form['user_type']
        location = request.form['location']
        location = location_formatting(location)

        user = Users(name=name, email=email, blood_group=blood_group, user_type=user_type, location=location)
        db.session.add(user)
        db.session.commit()

    return render_template('form.html')


@app.route('/nearest_users/<int:user_id>/<int:d>', methods=['GET'])
def get_nearest_users(user_id, d):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'})

    nearest_users = []
    for u in Users.query.filter(Users.id != user_id).all():
        latitude, longitude = user.location.split(', ')
        distance = calc_distance(float(latitude), float(longitude), float(u.location.split(', ')[0]), float(u.location.split(', ')[1]))
        if distance <= d:
            nearest_users.append({'id': u.id, 'name': u.name, 'distance': distance})

    nearest_users = sorted(nearest_users, key=lambda x: x['distance'])
    return jsonify(nearest_users)


def calc_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of Earth in km

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == '__main__':
    app.run(debug=True)
