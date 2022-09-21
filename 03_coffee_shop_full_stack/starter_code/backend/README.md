# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account (done)
2. Select a unique tenant domain (done)
3. Create a new, single page web application (done)
4. Create a new API (done) #dado 
   - in API Settings: (done)
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions: (done)
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista (done)
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager (done)
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other. (done)
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json` (done)
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors. (done)
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review! (done)

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## app endpoint :

#### /GET drinks



can use : 127.0.0.1 or localhost
```bash
localhost:5000/drinks
```
This endpoint don't require any authorization or authentification, it's public and work for all users.
the main function of this endpoint is to query the database ans show drinks in short format. (see models.py)
the output should be as follow :
json format :
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": "True"
}

#### /GET drinks-detail
```bash
localhost:5000/drinks-detail
```
this endpoint represent the recipe used in drinks, only Manager and Barista are configured to access the data behind this endpoint.
output should be :

{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}

### /POST drinks
 this endpoint is configured to be used only from manager, valid token is required to access the app and use this endpoint to create new drink
Authorization: Bearer <YOUR TOKEN>

The body should be in json format and respect the data structure.


### /Patch drinks/id

this endpoint is used to update  drink parameter referenced by : id. possibility to update title / recipe or both together.
Important : Only Manager is configured to access this endpoint and update data, for that make sure to have an active token for the manager or change the permission in the app if you are the admin of the auth0 account.
Example of update body :
Authorization: Bearer <YOUR TOKEN>
Request headers :
Content-Type      application/json
{
    "title": "Water5"
}

### /Delete drinks/id

Delete drink by id number of current drink in database.
Note that only manager is accepted to perform this action.

### POSTMAN 
-In this project, Postman was used for testing, and users are saved in collections, this is a simple app that demonstrates the use of Auth0 service with implementation in a python environment.

-Authentification and authorization condition is necessary to access the data or make any changes in the app data, Auth0 service account is necessary to generate a token "JWT". (JSON web token)

The security used in every endpoint for every user is JWT and stored in the front-end or can in local storage. you can copy paste the token into postman for test and choose bearer token as security check.
-- Where to find local storage : 
in your browser, click to inspect your page, search in the head bar for application. once clicked local storage is vaillable in a vertical bar. the address and the token are availlable (JWTS_LOCAL_KEY)
local host address for front-end: http://localhost:8100