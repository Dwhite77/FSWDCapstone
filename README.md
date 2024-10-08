# Casting Agency API

##URL 
https://fswdcapstone.onrender.com

## Project Overview
The Casting Agency API is a web application that allows users to manage actors and movies in a casting agency. The API provides endpoints for creating, reading, updating, and deleting actors and movies, as well as implementing role-based access control (RBAC) for different user roles.

## Motivation
The goal of this project is to build a robust API that can be used by a casting agency to manage their actors and movies efficiently. This project demonstrates the ability to create a RESTful API using Flask, SQLAlchemy, and Auth0 for authentication.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Auth0 account for authentication

##No installation required this should just work at the url
So long as it has been deployed on render

AUTH0_DOMAIN='dev-n2b3c216vvhww5je.us.auth0.com'

API_IDENTIFIER='Capstone'

AUTH0_CLIENT_ID='jkplYa7wJNDYAkCB82RqdErnjRR7Naex'

AUTH0_CLIENT_SECRET='QZWoaiHxC46zqOR_O3jYvt3Cw5kqJXXtdojr18NTafQqoakky5T9TYvDJP2j_ZhE'


###Authentication
To access the API, you need to obtain a JWT token from Auth0. Follow these steps:

Log in to your Auth0 dashboard.
Create a new application and configure the callback URL.
Use the client credentials to obtain a JWT token.
Include the token in the Authorization header of your requests:
Authorization: Bearer YOUR_JWT_TOKEN

# API Endpoints

## Actors

### GET /actors
Retrieves a list of actors.

### POST /actors
Adds a new actor.
**Request Body:**

{
  "name": "John Doe",
  "age": 30,
  "gender": "Male"
}
###PATCH /actors/<actor_id>
Updates an existing actor's information. Request Body:

{
  "name": "John Doe",
  "age": 30,
  "gender": "Male"
}
###DELETE /actors/<actor_id>
Deletes an actor.

##Movies
###GET /movies
Retrieves a list of movies.

###POST /movies
Adds a new movie. Request Body:

{
  "title": "Inception",
  "release_date": "2010-07-16"
}
###PATCH /movies/<movie_id>
Updates an existing movie's information. Request Body:

{
  "title": "Inception",
  "release_date": "2010-07-16"
}
###DELETE /movies/<movie_id>
Deletes a movie.


##Role-Based Access Control (RBAC)
The API implements RBAC to restrict access based on user roles. The following roles are defined:

Casting Assistant: Can view actors and movies.
Director: Can add and update actors and movies.
Producer: Can delete actors and movies.
Testing
To run the tests, use the following command:


Retrieving actors
Adding actors
Handling errors for missing data
Role-based access control
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Flask
SQLAlchemy
Auth0

### Key Sections Explained:
- **Project Overview**: Brief description of the project and its purpose.
- **Motivation**: Explanation of why the project was created.
- **Getting Started**: Instructions on prerequisites, installation, and running the application.
- **Authentication**: Details on how to authenticate with the API.
- **API Endpoints**: Documentation of the available API endpoints and their expected inputs/outputs.
- **Role-Based Access Control (RBAC)**: Explanation of the roles and their permissions.
- **Testing**: Instructions on how to run tests for the project.
- **License and Acknowledgments**: Information about the project's license and any libraries or tools used.