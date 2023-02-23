import jwt
import time

from math import radians, sin, cos, sqrt, atan2
from arcgis.geocoding import geocode, reverse_geocode
from werkzeug import security


def generate_hash(password):
    return security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)


def create_jwt_token(user_id, secret):
    token_expiry_time_hours = 1
    payload = {'user_id': user_id,
               'exp': int(time.time()) + (token_expiry_time_hours * 60 * 60)}
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def location_formatting(address):
    """
    This function changes the text location into geographical coordinates
    Note: arcgis api returns coordinates in format x:longitude, y:latitude
    """
    geocoded_adr = geocode(address)
    latitude = geocoded_adr[0]['location']['y']
    longitude = geocoded_adr[0]['location']['x']
    return '{}, {}'.format(latitude, longitude)


def calc_distance(lat1, lon1, lat2, lon2):
    """
    Haversine formula for calculating distance between 2 geographical points
    """
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