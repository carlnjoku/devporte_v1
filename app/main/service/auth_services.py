from flask import Flask, request, jsonify, make_response
import uuid
import datetime

from app.main import mongo
from bson.objectid import ObjectId

from app.main import mongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from ..config import key




#token = jwt.encode({'userId':user['_id'], 'email':user['email'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=30)}, app.config['SECRET_KEY'])
#return jsonify({'token': token.decode('UTF-8'), 'user_type' : user['user_type'], 'email': user['email'], 'userId':user['_id'], 'loggedIn': True})

#generate token 
def generate_token(user):
    print(user)
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401




class Auth:   
    @staticmethod 
    def login(auth):
       
        if not auth or not auth['username'] or not auth['password']:
            response_object = {
                'status':'fail',
                'message':''
            }
            return ('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})

        user = mongo.db.users.find_one({"email": auth['username']})
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
            #return jsonify({'message':'Could not verify account'})
    
        if check_password_hash(user['password'], auth['password']):
            
            #generate token 
            token = jwt.encode({'_id': user['_id'],  'email':user['email'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=30)}, key)
        
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'data': token.decode('UTF-8'), 'user_type' : user['user_type'], 'email': user['email'], '_id':user['_id'], 'confirm_email':user['confirm_email'], 'professional_title':user['professional_title'], 'loggedIn': True
            }
            print(response_object)
            return response_object, 200
        
        #return jsonify({'message':'Could not verify account'})
        return make_response('Could not verify1', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
    
    @staticmethod
    def get_loggedin_user(new_request):
        user_type = request.args.get('user_type')
        print(user_type)
        #auth_token = new_request.headers.get('x-access-token')
        #print(auth_token)
        
        if new_request['user_type'] != 'employer':
            response_object = {
                "status":"fail",
                "message": "Unauthorized"
            }
            return response_object, 401
        return jsonify({'message': 'welcome back'}), 200


    @staticmethod
    def get_loggedin_user1(auth_header):
        print(auth_header)
        # get the auth token
        auth_token = auth_header.headers.get('x-access-token')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
