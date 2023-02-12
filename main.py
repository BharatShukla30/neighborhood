from flask import Flask, request, render_template
import sqlite3

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
        location = request.form['location'] if user_type == 'Organization' else None

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (name, email, blood_group, user_type, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, blood_group, user_type, location))
        conn.commit()
        conn.close()

        return 'User registered successfully!'

    return '''
        <form method="post">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" class="form-control" id="name" name="name">
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" class="form-control" id="email" name="email">
            </div>
            <div class="form-group">
                <label for="blood_group">Blood Group:</label>
                <select class="form-control" id="blood_group" name="blood_group">
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                </select>
            </div>
            <div class="form-group">
                <label for="user_type">I am a:</label>
                <select class="form-control" id="user_type" name="user_type">
                    <option value="Individual">Individual</option>
                    <option value="Organization">Organization</option>
                </select>
            </div>
            <div class="form-group">
                <label for="location">Location:</label>
                <input type="text" class="form-control" id="location" name="location"
                    style="display: none;">
                <input type="button" class="form-control btn btn-primary" value="Get Location"
                    id="get-location" style="display: none;">
            </div>
            <script>
                document.getElementById("user_type").addEventListener("change", function() {
                    var location = document.getElementById("location");
                    var getLocation = document.getElementById("get-location");
                    if (this.value === "Organization") {
                        location.style.display = "block";
                        getLocation.style.display = "none";
                    } else {
                        location.style.display = "none";
                        getLocation.style.display = "block";
                    }
                });

                document.getElementById("get-location").addEventListener("click", function() {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        document.getElementById("location").value =
                            position.coords.latitude + ", " + position.coords.longitude;
                    });
                });
            </script>
            <button type="submit" class="btn btn-primary">Register</button>
            </form>
'''
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
