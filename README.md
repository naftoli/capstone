# Capstone Project
This project is the final project of the Udacity Full Stack Developer Nano Degree Program. The goal of this project is to deploy a Flask application with Heroku/PostgreSQL and enable Role Based Authentication and roles-based access control (RBAC) with Auth0 (third-party authentication systems).

The project I created is for creating and editing Users and their Favorite Links

## Getting Started
### Installing Dependencies
#### Python 3.11
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
- [Auth0](https://auth0.com/) is the third-party authentication system we'll use to handle user authentication and roles-based access control (RBAC).
- [PostgreSQL](https://www.postgresql.org/) is the database we'll use to store our data.
- [Heroku](https://www.heroku.com/) is the cloud platform we'll use to deploy our application.
- [Postman](https://www.postman.com/) is the application we'll use to test our endpoints.
- [Python3](https://www.python.org/) is the language we'll use to develop our application.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is the extension we'll use to handle SQLAlchemy database migrations.
- [Flask-Script](https://flask-script.readthedocs.io/en/latest/) is the extension we'll use to handle SQLAlchemy database migrations.
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) is the extension we'll use to handle RESTful APIs. 

## Running the server
Make sure you are working using your created virtual environment.

To run the server, execute:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```
Sourcing the `setup.sh` file will set the environment variables needed to run the application.
Setting the `FLASK_ENV` variable to `development` will detect file changes.
Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application.

## Testing
To run the tests, run
```bash
source setup.sh
python test_app.py
```

## API Reference
### Getting Started
- Base URL: This application is hosted on Heroku and can be accessed at https://naftoli.herokuapp.com/
- Authentication: This application users Auth0 for authentication and authorization. The following endpoint is used to authenticate: 
    - https://naftoli.herokuapp.com/login
- This endpoint will redirect to Auth0's login page
- After logging in, the user will be redirected to the following endpoint:
    - https://naftoli.herokuapp.com/login-results
    - This endpoint will set the user's JWT token in a session variable
- RBAC: This application has the following roles:
    - Admin
        - Can create, read, update, and delete Users
        - Can create, read, update, and delete Favorite Links
    - User
        - Can read Users and Favorite Links
- The following users are available for testing:
    - Admin
        - Username: admin@gmail.com
        - Password: admin@5783!
    - User
        - Username: user@gmail.com
        - Password: user@5783!

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```

The API will return the following error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 500: Internal Server Error
- AuthError: Auth0 Error

### Endpoints
#### GET /
- If user is logged in, routes to '/users' endpoint
- Otherwise, routes to login page

#### GET /users
- Returns a list of users
- Requires the `get:users` permission

#### GET /users/<int:user_id>
- Returns a user with the given id
- If no such user exists, returns a 400 error
- Requires the `get:users` permission

#### POST /users
- Creates a new user
- Returns the user that was created
- Requires the `post:users` permission

#### PATCH /users/<int:user_id>
- Updates a user with the given id
- Returns the user that was updated
- If no such user exists, returns a 400 error
- Requires the `patch:users` permission

#### DELETE /users/<int:user_id>
- Deletes a user with the given id
- If no such user exists, returns a 400 error
- Requires the `delete:users` permission

#### POST /users/<int:user_id>/favorites
- Creates a new favorite link for the user with the given id
- Returns the favorite link that was created
- If no such user exists, returns a 400 error
- Requires the `post:favorites` permission

#### PATCH /users/<int:user_id>/favorites/<int:favorite_id>
- Updates a favorite link with the given id for the user with the given id
- Returns the favorite link that was updated
- If no such user or favorite link exists, returns a 400 error
- Requires the `patch:favorites` permission

#### DELETE /users/<int:user_id>/favorites/<int:favorite_id>
- Deletes a favorite link with the given id for the user with the given id
- If no such user or favorite link exists, returns a 400 error
- Requires the `delete:favorites` permission

## Authors
Naftoli Rapoport