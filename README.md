# Casting Agency API

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

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Dwhite77/FSWDCapstone.git
   cd casting-agency
Install the required packages:

pip install -r requirements.txt
Set up the database:

Create a new database in your preferred SQL database management system.
Update the database connection string in config.py.
Set up environment variables for Auth0: Create a .env file and add the following:

AUTH0_DOMAIN='your-auth0-domain'
API_IDENTIFIER='your-api-identifier'
JWT_SECRET='your-jwt-secret'
Running the Application
To run the application, use the following command:

flask run
The API will be available at http://127.0.0.1:5000.

Authentication
To access the API, you need to obtain a JWT token from Auth0. Follow these steps:

Log in to your Auth0 dashboard.
Create a new application and configure the callback URL.
Use the client credentials to obtain a JWT token.
Include the token in the Authorization header of your requests:
Authorization: Bearer YOUR_JWT_TOKEN
API Endpoints
Actors
GET /actors

Retrieves a list of actors.
POST /actors

Adds a new actor.
Request Body:
{
  "name": "John Doe",
  "age": 30,
  "gender": "Male"
}
PATCH /actors/<actor_id>

Updates an existing actor's information.
DELETE /actors/<actor_id>

Deletes an actor.
Movies
GET /movies

Retrieves a list of movies.
POST /movies

Adds a new movie.
PATCH /movies/<movie_id>

Updates an existing movie's information.
DELETE /movies/<movie_id>

Deletes a movie.
Role-Based Access Control (RBAC)
The API implements RBAC to restrict access based on user roles. The following roles are defined:

Casting Assistant: Can view actors and movies.
Director: Can add and update actors and movies.
Producer: Can delete actors and movies.
Testing
To run the tests, use the following command:

python -m unittest discover
Test Cases
The test suite includes tests for:

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