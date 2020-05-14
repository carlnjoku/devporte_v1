from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='Authorisation related operations')

    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password')
    })

    

    


    