import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String

print("testing....")

database_path = os.environ['DATABASE_URL']
print("dbpath")
db = SQLAlchemy()
print("db = sql done")

"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_SECRET_KEY'] = os.environ[JWT_SECRET_KEY] # Change this to a random secret key
    db.app = app
    db.init_app(app)
    db.create_all()
"""
def setup_db(app):
    # Set the database URI for SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Ensure JWT_SECRET_KEY is accessed from environment variables correctly
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_random_secret_key')  # Provide a default if not set
    
    # Initialize the app with the database
    db.app = app
    db.init_app(app)
    
    # Create all tables
    with app.app_context():
        db.create_all()

print("post setup_db")

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f'<Movie {self.title}>'

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f'<Actor {self.name}>'
