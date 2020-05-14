from flask import request
from flask_restplus import Resource
from app.main.service.auth_services import Auth
from ..model.authDto import AuthDto




api = AuthDto.api
user_auth = AuthDto.user_auth



@api.route('/login')
@api.response(201, 'Login successful')
@api.doc('User login endpoint')
class UserLogin(Resource):
    @api.expect(user_auth, validate=True)
    def post(self):
        data = request.json
        print(data)
        return Auth.login(auth=data)

    
@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        return Auth.login(data=auth_header)









