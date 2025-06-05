"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint 
from api.models import db, User, Invoice
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/token", methods=["POST"])
def generate_token():
    #login credentials
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    #query the database if the user email exists
    email = email.lower()
    user = db.session.get(User, email)

    # craete a condition if the user doesnt exist
    if user is None:
        raise APIException('Sorry email or password not found', status_code=404)
    elif user is not None and user.password != password:
        raise APIException('Sorry email or password not found', status_code=404)

        
   #if the user does exist
    access_token = create_access_token(identity=user.id)
    response={
        'access_token': access_token,
        'user_id': user.id,
        'message': f'Welcome{user.email}!'
    }
    return jsonify(response), 200

#create a signup route test on postman
#

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200