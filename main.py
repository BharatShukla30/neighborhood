import utilities.utils as utils
import secrets

from werkzeug import security
from constants import ARCGIS_URL, ARCGIS_API_KEY
from model.User import db, Users
from flask import Flask, request, render_template, jsonify
from arcgis.gis import GIS
from flask_cors import CORS
from exceptions.CustomException import DatabaseError


gis = GIS(ARCGIS_URL, api_key=ARCGIS_API_KEY)
app = Flask(__name__)
CORS(app, origins='*', supports_credentials=True)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        user = Users.query.filter_by(email=email).first()
        if user is None or not security.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # create a JWT token
        token = utils.create_jwt_token(user.id, app.secret_key)

        return jsonify({'token': token})
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        blood_group = request.json.get('blood_group')
        user_type = request.json.get('user_type')
        location = request.json.get('location')
        password = request.json.get('password')
        hash_password = utils.generate_hash(password)
        location = utils.location_formatting(location)
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            return "Email already exists!!",
        user = Users(name=name, email=email, password=hash_password, blood_group=blood_group, user_type=user_type,
                     location=location)
        db.session.add(user)
        db.session.commit()
        response = jsonify({'message': 'Registration successful'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    return render_template('form.html')


@app.route('/nearest_users/<int:user_id>/<int:d>', methods=['GET'])
def get_nearest_users(user_id, d):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'})

    nearest_users = []
    for u in Users.query.filter(Users.id != user_id).all():
        latitude, longitude = user.location.split(', ')
        nearest_user_latitude = u.location.split(', ')[0]
        nearest_user_longitude = u.location.split(', ')[1]
        distance = utils.calc_distance(float(latitude), float(longitude), float(nearest_user_latitude),
                                       float(nearest_user_longitude))
        if distance <= d:
            nearest_users.append({'id': u.id, 'name': u.name, 'distance': distance, 'latitude': nearest_user_latitude,
                                  'longitude': nearest_user_longitude})

    nearest_users = sorted(nearest_users, key=lambda x: x['distance'])
    return jsonify(nearest_users)


if __name__ == '__main__':
    app.run(debug=True, port=8001)
