import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Database setting up - creation
'''
db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#postman test without Auth0 and no data: 200!
# @app.route('/test')
# def get_test():
    
#     return 'this is just a test'
#==================================
#get drinks
@app.route('/drinks', methods=['GET'])
#@requires_auth('get:drinks') #authentication not required for drink
def get_drinks(): #payload fron auth.py 
    #payload is a decoded jwt 
    try:
        #query database to get drinks from Drink table
        query_drinks = Drink.query.order_by(Drink.id).all()
        if not query_drinks: #if data not found
            abort(404)
        #short is declared in models.py for short representation of drinks   
        drinks = [drink.short() for drink in query_drinks]
        print(drinks)
        return jsonify({
            "success": "True",
            "drinks": drinks
        })
    except Exception as e:
        print(e)
        abort(400)




'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission ----important
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#first let's make the endpoint work with long representation of drinks detail, then we add Auth0 permission

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    #print(payload)
    try:    
        #query database to get drinks from Drink table
        query_drinks = Drink.query.all()
        if not query_drinks: #if data not found
            abort(404)
        drinks = [drink.long() for drink in query_drinks]  
        #print(drinks, "-------")  

        return jsonify(
            {
                "success": True,
                "drinks" : drinks
            }
        )
        #if error; print reason for failure
    except Exception as e :
        print(e)
        abort(400)

'''
@Done implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    #first let's set up a format to add our drink
    body = request.get_json()
    if not body:
        abort(400)
    # adding Title / Recipe to the table
    new_title = body.get('title')
    new_recipe = body.get('recipe')   #not null
    print(new_title)
    print(new_recipe)
    
    try:
      drink = Drink(title=new_title, recipe = json.dumps(new_recipe))   
      #print(drink)
      drink.insert() #insert to database

      return jsonify(
        {
            "success": True,
            "drinks": drink.long()
        }
      ) 
    except Exception as e:
        abort(422)
'''
@Done implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    print(drink, "=======patch")
    if not drink:
        abort(404)
    
    updated_title = body.get('title')
    updated_recipe = body.get('recipe')
    try :
        #without if statement it will show null- so that the app can update only title/recipe or both
        if updated_recipe:    
            #json.dumps is important to contain the updated recipe in the right accepted json format 
            drink.recipe= json.dumps(updated_recipe)
        
        
        #condition if ,- if title is updated-
        if updated_title:
            drink.title = updated_title
        
        # print(updated_title,"*********")
        # print(updated_recipe,"8888888")
        drink.update()
        drink_up = [drink.long()]
        return jsonify(
            {
                "success" : True,
                "drink" : drink_up
            }
        )
    except:
        abort(400)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    body = request.get_json()
    #get the drink to be deleted
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    print(drink)
    #drink id to delete is not availlable, "not found" in DB
    if not drink:
        abort(404) 
    try:
        drink.delete()
        drink_up = [drink.long()]
        return jsonify(
            {
                "success" : True,
                "deleted" : drink.id
            }
        ) 
    except:
        #appropriate code for failling
        abort(422)    
# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422




'''
@done implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
#Auth error from auth.py 
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code