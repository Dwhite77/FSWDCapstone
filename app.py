from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, Movie, Actor
from functools import wraps

from models import setup_db

print("app")
app = Flask(__name__)
setup_db(app)
print("appsetup")

# Initialize JWT Manager
jwt = JWTManager(app)

# Role-based access control decorator
def requires_auth(permission=''):
    def decorator(f):
        @wraps(f)
        @jwt_required()  # Protect the route with JWT
        def decorated_function(*args, **kwargs):
            # Get the identity of the current user
            current_user = get_jwt_identity()
            # Check if the user has the required permission
            if permission not in current_user['permissions']:
                return jsonify({'message': 'Permission denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
@app.route('/add_actor', methods=['GET', 'POST'])
@requires_auth('add:actor')  # Protect this route
def add_actor_page():
    if request.method == 'POST':
        data = request.form
        new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
        db.session.add(new_actor)
        db.session.commit()
        return jsonify({'message': 'Actor added'}), 201
    return render_template('add_actor.html')  # Ensure add_actor.html is in the templates folder

# Route to render the add movie page
@app.route('/add_movie', methods=['GET', 'POST'])
@requires_auth('add:movie')  # Protect this route
def add_movie_page():
    if request.method == 'POST':
        data = request.form
        new_movie = Movie(title=data['title'], release_date=data['release_date'])
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({'message': 'Movie added'}), 201
    return render_template('add_movie.html')  # Ensure add_movie.html is in the templates folder

# Start the application
if __name__ == '__main__':
    app.run(debug=True)