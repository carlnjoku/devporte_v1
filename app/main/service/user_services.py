from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import json
import os

from app.main import mongo
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from ..config  import gateway 



from ..config import key
from app.main.service.sendemail_service import send_email_confirmation
from app.main.utils.file_upload import upload_profile




def get_user_minimal_info(current_user):
    if current_user['user_type'] != current_user:
        response_object = {
            "status":"fail",
            "message": "Unauthorized"
        }
        return response_object, 401
    return jsonify({'message': 'welcome back'}), 200



def signup(data):
    try:
        # Check if user exists already 
        email = data['email']
        
        member = mongo.db.users.find_one({"email": email}, {"_id": 0})
        if member is not None:
            response_object = {
                'status': 'success',
                'data': 'User already exists. Please Log in.',
            }
            return response_object, 409

        else:
            data['_id'] = str(ObjectId())
            data['publicId'] = str(uuid.uuid4())
            data['confirm_email'] = False
            data['professional_title'] =''
            data['password'] = generate_password_hash(data['password'], method='sha256')
            
            _id = mongo.db.users.insert_one(data).inserted_id
    
            new_data = {
                '_id': _id, 
                'email': data['email'], 
                'firstname': data['firstname'],
                'lastname': data['lastname'],
                'user_type': data['user_type'],
                'confirm_email': data['confirm_email'],
                'professional_title': data['professional_title']
                
            }
            send_email_confirmation(new_data)
            response_object = {
                'status': 'success',
                'data': new_data
            }
        return response_object, 201

    except Exception as e:
        response_object = {
                'status': 'fail',
                'data': e
            }
        return response_object, 500

def do_email_confirmation(_id):
    try:
        print(_id)
        member = mongo.db.users.find_one({"_id": _id})
        if member is not None:
            mongo.db.users.update({"_id": _id}, {"$set": {'confirm_email':True}})
            response_object = {
                'status': 'success',
                'message': 'Email confirmed successfully'
            }
            return response_object
        else:
            response_object = {
                'status': 'fail',
                'message': 'Users does not exist'
            }
            return response_object, 404
            
    except Exception as e:
        
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong, try again'
        }
        return response_object, 500
    
    
def get_skills():
    try:
        tech = mongo.db.technologies.find({}, {'_id': 0, 'tool_name':1})
        print(tech.count())
        #return jsonify({"data": candidates.count()})
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return jsonify({"data": list(tech)})
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})
   

def update_profile(data, upload):
    print(data)
    print(upload)
    user = mongo.db.users.find_one({"_id": data['_id']})
    if user is not None:
        
        # Upload the profile avatar
        firstname = "Carl"
        userId = data['_id']
        uploaded_file =  upload_profile(upload, firstname, userId)

        data['avatar'] = uploaded_file
        x = mongo.db.users.update_one({"_id": data['_id']}, {'$set':data})
        response_object = {
            'status': 'success',
            'message': 'Profile updated uccessfully.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        return response_object, 404



def get_all_users():
    return mongo.db.users1.find({})


def get_a_user(_id):
    user = mongo.db.users.find_one({"_id":_id})
    if user is not None:
        response_object = {
            'status': 'success',
            'data': user
        }
        print(user)
        return response_object, 201
    else:

        response_object = {
            'status': 'fail',
            'message': 'This user does not exist or has been deleted'
        }
        return response_object

def get_an_employer_intro():
    user = mongo.db.users.find_one({"_id":_id}, {"_id":1, "avatar":1, "email":1, "company_name":1, "firstname":1, "lastname":1, "country":1,})
    if user is not None:
        response_object = {
            'status': 'success',
            'data': user
        }
        print(user)
        return response_object, 201
    else:

        response_object = {
            'status': 'fail',
            'message': 'This user does not exist or has been deleted'
        }
        return response_object

def change_password(data):
    user = mongo.db.users.find_one({"_id":data['_id']})
    if user is not None:
        new_password = generate_password_hash(data['new_password'], method='sha256')
        mongo.db.users.update({'_id':data['_id']}, {'$set':{'password':new_password}})
        response_object = {
            'status': 'success',
            'data': 'Password has been changed successfully'
        }
        print(user)
        return response_object, 201
    else:

        response_object = {
            'status': 'fail',
            'message': 'This user does not exist or has been deleted'
        }
        return response_object


# EMPLOYER
def update_employer_contact(data):
    try:
        user = mongo.db.users.find_one({"_id":data['_id']})
        print(user)
        if user is not None:
            mongo.db.users.update({'_id':data['_id']}, {'$set':data})
            
            response_object = {
                'status': 'success',
                'data': data
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'data': 'User does not exist'
            }
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'fail',
            e: 'Something went wrong, try again'
        }
        return response_object, 500


###################
# PAYMENT           #
###################

