import sqlite3
import re

from constants import ARCGIS_URL, ARCGIS_API_KEY
from flask import Flask, request, render_template
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode

gis = GIS(ARCGIS_URL, api_key = ARCGIS_API_KEY)
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            blood_group TEXT,
            user_type TEXT,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

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
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (name, email, blood_group, user_type, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, blood_group, user_type, location))
        conn.commit()
        conn.close()

        return 'User registered successfully!'

    return render_template('form.html')
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
