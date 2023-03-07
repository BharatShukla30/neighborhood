import utilities.utils as utils
import secrets

from utilities.ApiResponse import ApiResponse
from werkzeug import security
from constants import ARCGIS_URL, ARCGIS_API_KEY
from model.User import db, Users
from model.User_location import db, User_location
from flask import Flask, request, render_template, jsonify
from arcgis.gis import GIS
from flask_cors import CORS
from exceptions.CustomException import DatabaseError
from utilities.decorators import login_required

gis = GIS(ARCGIS_URL, api_key=ARCGIS_API_KEY)
app = Flask(__name__)
CORS(app, origins='*', supports_credentials=True, resources={r"/*": {"origins": "*"}})
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
        email = request.json.get('email').lower()
        password = request.json.get('password')

        user = Users.query.filter_by(email=email).first()
        if user is None or not security.check_password_hash(user.password, password):
            return ApiResponse(status=401, message="Invalid user or wrong password").__dict__

        # create a JWT token
        token = utils.create_jwt_token(user.id, app.secret_key)

        return ApiResponse(status=200, data=token).__dict__
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        isRegistered = True
        name = request.json.get('name')
        email = request.json.get('email').lower()
        blood_group = request.json.get('blood_group')
        user_type = request.json.get('user_type')
        location = request.json.get('location')
        password = request.json.get('password')
        city = request.json.get('city')
        state = request.json.get('state')

        hash_password = utils.generate_hash(password)
        location = utils.location_formatting(location)
        user = Users.query.filter_by(email=email).first()
        

        if user is not None:
            response = jsonify({'message': 'Registration Failed, user already exists'})
            response.status_code = 401
        else:
            user = Users(name=name, email=email, password=hash_password, blood_group=blood_group, user_type=user_type,
                         location=location)
            user_location = User_location(city = city, state = state, location = location)

            db.session.add(user)
            db.session.add(user_location)
            db.session.commit()
            response = jsonify({'message': 'Registration successful'})

        # Set the Access-Control-Allow-Origin header dynamically based on the origin of the request
        if 'Origin' in request.headers:
            origin = request.headers['Origin']
            response.headers.add('Access-Control-Allow-Origin', origin)

        # Set the Access-Control-Allow-Credentials header
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    return render_template('form.html')


@app.route('/nearest_users/<int:d>', methods=['GET'])
@login_required
def get_nearest_users(user_id, d):
    user = Users.query.get(user_id)

    if user is None:
        return ApiResponse(status=500, message="User not found").__dict__

    nearest_users = []
    for u in Users.query.filter(Users.id != user_id).all():
        latitude, longitude = user.location.split(', ')
        nearest_user_latitude = u.location.split(', ')[0]
        nearest_user_longitude = u.location.split(', ')[1]
        distance = utils.calc_distance(float(latitude), float(longitude), float(nearest_user_latitude),
                                       float(nearest_user_longitude))
        if distance <= d:
            nearest_users.append({'id': u.id, 'distance': distance, 'latitude': nearest_user_latitude,
                                  'longitude': nearest_user_longitude})
            
        latitude, longitude = user.location.split(', ')
        nearest_user_latitude = u.location.split(', ')[0]
        nearest_user_longitude = u.location.split(', ')[1]


    nearest_users = sorted(nearest_users, key=lambda x: x['distance'])
    return ApiResponse(status=200, data=nearest_users).__dict__


@app.route('/get_user_details', methods=['GET'])
@login_required
def get_user_info(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return ApiResponse(status=501, message="User is not available").__dict__
    user_info = {
        'id': user.id,
        'name': user.username,
        'email': user.email,
        'user_type': user.user_type,
        'blood_group': user.blood_group,
        'location': user.location
        }
    return ApiResponse(status=200, data=user_info).__dict__


if __name__ == '__main__':
    app.run(debug=True, port=8001)