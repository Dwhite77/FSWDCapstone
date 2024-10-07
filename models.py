import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date
import json

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

print(os.environ.get('JWT_SECRET_KEY'))
print(os.environ['JWT_SECRET_KEY'])
print(database_path)

print("post setup_db")

class Movie(db.Model):

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    release_date = Column(String(10), nullable=False)


    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f'<Movie {self.title}>'

class Actor(db.Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f'<Actor {self.name}>'