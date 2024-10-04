from flask import Flask, jsonify, request, render_template, redirect, session, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, Movie, Actor, setup_db
from functools import wraps
import os
from auth.auth import requires_auth


print("app")
app = Flask(__name__)
setup_db(app)
print("appsetup")

# Initialize JWT Manager
jwt = JWTManager(app)


# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the templates folder

# Define your API routes here
@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.name for actor in actors])

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.title for movie in movies])

@app.route('/actors', methods=['POST'])
@requires_auth('add:actor')  # Protect this route
def add_actor():
    data = request.get_json()
    new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify({'message': 'Actor added'}), 201

@app.route('/movies', methods=['POST'])
@requires_auth('add:movie')  # Protect this route
def add_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], release_date=data['release_date'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'Movie added'}), 201

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')  # Protect this route
def delete_actor(id):
    actor = Actor.query.get(id)
    if actor:
        db.session.delete(actor)
        db.session.commit()
        return jsonify({'message': 'Actor deleted'}), 200
    return jsonify({'message': 'Actor not found'}), 404

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movie')  # Protect this route
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie deleted'}), 200
    return jsonify({'message': 'Movie not found'}), 404

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('update:actor')  # Protect this route
def update_actor(id):
    actor = Actor.query.get(id)
    if actor:
        data = request.get_json()
        actor.name = data.get('name', actor.name)
        actor.age = data.get('age', actor.age)
        actor.gender = data.get('gender', actor.gender)
        db.session.commit()
        return jsonify({'message': 'Actor updated'}), 200
    return jsonify({'message': 'Actor not found'}), 404

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('update:movie')  # Protect this route
def update_movie(id):
    movie = Movie.query.get(id)
    if movie:
        data = request.get_json()
        movie.title = data.get('title', movie.title)
        movie.release_date = data.get('release_date', movie.release_date)
        db.session.commit()
        return jsonify({'message': 'Movie updated'}), 200
    return jsonify({'message': 'Movie not found'}), 404



# Route to render the add actor page
@app.route('/add_actor', methods=['GET'])
def add_actor_page():
    return render_template('add_actor.html')  # Ensure add_actor.html is in the templates folder

# Route to render the add movie page
@app.route('/add_movie', methods=['GET'])
def add_movie_page():
    return render_template('add_movie.html')  # Ensure add_movie.html is in the templates folder

@app.route('/callback')
def callback():
    # Here you would typically handle the token returned by Auth0
    # For example, you might store it in the session
    token = request.args.get('access_token')
    session['jwt_token'] = token  # Store the token in the session
    return redirect(url_for('index'))  # Redirect to the home page or another page


app.secret_key = os.environ['JWT_SECRET_KEY']  # Make sure to set this in your .env file

@app.route('/login')
def login():
    return redirect(f"https://{os.environ['AUTH0_DOMAIN']}/authorize?audience={os.environ['API_IDENTIFIER']}&response_type=token&client_id={os.environ['AUTH0_CLIENT_ID']}&redirect_uri={url_for('callback', _external=True)}")


# Start the application
if __name__ == '__main__':
    app.run(debug=True)