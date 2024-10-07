from flask import Flask, jsonify, request, render_template, redirect, session, url_for, abort
from models import db, Movie, Actor, setup_db
from flask_cors import CORS
import os
import requests
from auth.auth import requires_auth




app = Flask(__name__)
setup_db(app)
app.secret_key = os.environ.get("JWT_SECRET_KEY", "default_secret_key")
print(app.secret_key)
CORS(app)


# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response


# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html', session=session.get('jwt_token'))

# Define your API routes here
@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return render_template('actor.html', actors=actors)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return render_template('movie.html', movies=movies)

@app.route('/actors', methods=['POST'])
@requires_auth('add:actor')  # Protect this route
def add_actor(payload):
    print(payload)
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")

    if not name or not age or not gender:
        abort(400)

    try:
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return render_template('index.html')

    except Exception as e:
        print(f"Error making actor: {e}")
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('add:movie')  # Protect this route
def add_movie():

    title = request.form.get("title")
    release_date = request.form.get("release_date")

    if not title or release_date:
         abort(400)

    try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return render_template('index.html')
    except Exception as e:
        print(f"Error making movie: {e}")
        abort(422)



@app.route('/delete-actor/<int:actor_id>', methods=['POST'])
#@requires_auth('delete:actor')  # Protect this route
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        db.session.delete(actor)
        db.session.commit()
    return redirect('/actors')


@app.route('/delete-movie/<int:movie_id>', methods=['POST'])
#@requires_auth('delete:movie')  # Protect this route
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect('/movies')

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



@app.route('/callback', methods=["GET", "POST"])
def callback():
    code = request.args.get('code')
    token_url = f'https://{os.environ["AUTH0_DOMAIN"]}/oauth/token'
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': os.environ['AUTH0_CLIENT_ID'],
        'client_secret': os.environ['AUTH0_CLIENT_SECRET'],
        'code': code,
        'redirect_uri': url_for('callback', _external=True)
    }
    token_headers = {'Content-Type': 'application/json'}
    token_response = requests.post(token_url, json=token_payload, headers=token_headers)
    tokens = token_response.json()

    # Store the access token in the session
    session['jwt_token'] = tokens.get('access_token')
    return redirect(url_for('index'))


@app.route('/gettoken')
def get_token():
    token = request.args.get('#access_token')
    print(token)
    session['jwt_token'] = token
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return redirect(
        f"https://{os.environ['AUTH0_DOMAIN']}/authorize"
        f"?audience={os.environ['API_IDENTIFIER']}"
        f"&response_type=code"
        f"&client_id={os.environ['AUTH0_CLIENT_ID']}"
        f"&redirect_uri={url_for('callback', _external=True)}"
    )


# Start the application
if __name__ == '__main__':
    app.run(debug=True)