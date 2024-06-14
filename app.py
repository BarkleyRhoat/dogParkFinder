from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, DogPark

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate here

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

app = create_app()
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@app.route('/nearest_park', methods=['POST'])
@login_required
def nearest_park():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    api_key = app.config['TOMTOM_API_KEY']
    search_url = f"https://api.tomtom.com/search/2/nearbySearch/.json?key={api_key}&lat={latitude}&lon={longitude}&radius=5000&categorySet=7315"

    response = requests.get(search_url)
    parks = response.json().get('results', [])

    if parks:
        nearest_park = parks[0]
        park_info = {
            'name': nearest_park['poi']['name'],
            'latitude': nearest_park['position']['lat'],
            'longitude': nearest_park['position']['lon'],
            'address': nearest_park.get('address', {}).get('freeformAddress', 'No address available')
        }
    else:
        park_info = None

    return render_template('profile.html', name=current_user.username, park=park_info)

if __name__ == '__main__':
    app.run(debug=True)
