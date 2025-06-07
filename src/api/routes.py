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
    user = User.query.filter_by(email=email).first()

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
        'message': f'Welcome {user.email}!'
    }
    return jsonify(response), 200

#create a signup route test on postman
@api.route('/signup', methods=['POST'])
def registered_user():
    email= request.json.get('email')
    password= request.json.get('password')

#query the database to chek if the email already exists
    email = email.lower()
    user = User.query.filter_by(email=email).first()

#chk if the user email already exists
    if user is not None and user.email == email:
        response = {
            'message': f'{user.email} already exists. Please login.'
        }
        return jsonify(response), 403
    new_user = User()
    new_user.email= email
    new_user.password = password
    new_user.is_active = True
    db.session.add(new_user)
    db.session.commit()

    response = {
        'message': f"Awesome {new_user.email}! You have successfully signed up! please login"
    }
    return jsonify(response), 201



# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()


def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200