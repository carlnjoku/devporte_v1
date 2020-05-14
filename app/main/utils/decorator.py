from flask_restplus import Api
from flask import request, make_response
from functools import wraps

from app.main import mongo
from bson.objectid import ObjectId
import jwt

from ..config import key

from app.main.service.auth_services import  Auth


def token_required_1(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.login(request)
        token = data.get('data')
        print('Yoyo'+token)
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            response_object = {
                'status':'',
                'message': 'Token missing!'
            }
            return response_object, 403
            print(token)
            ('hey boby')
        try:
            data = jwt.decode(token, key)
            current_user = mongo.db.users.find_one({"_id": data['_id']})
            print('pop' + current_user)

        except :
            #return jsonify({'msg':'Token is not valid'})
            #return jsonify({"data": {"error_msg": str(e)}})
            return make_response('Token is not valid', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
            
        return f(current_user, *args, **kwargs)
    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #Auth.get_loggedin_user(request)
        
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
            
        if not token:
            response_object = {
                "status":"fail",
                "data":"Token missing!"
            }
            return response_object , 403
          
        try:
            data = jwt.decode(token, key)
            current_user = mongo.db.users.find_one({"_id": data['_id']})
            

        except :
            #return jsonify({'msg':'Token is not valid'})
            #return jsonify({"data": {"error_msg": str(e)}})
            return make_response('Token is not valid', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
            
        return f(current_user, *args, **kwargs)
    return decorated
