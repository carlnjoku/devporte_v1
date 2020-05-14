from flask_restplus import Namespace, fields
import json



class SocketDto:
    api = Namespace('user', description='User operations including create, edit, view and delete')

    signup = api.model('signup details', {
        'email': fields.String(required=True, description='user email address'),
        'firstname': fields.String(required=True, description='user firstname'),
        'lastname': fields.String(required=True, description='user last name'),
        'user_type': fields.String(required=True, description='user type'),
        'country': fields.String(required=True, description='user type'),
        'company_name': fields.String(required=False, description='user type'),
        'state': fields.String(required=True, description='user type'),
        'password': fields.String(required=True, description='user password'),
       
    })