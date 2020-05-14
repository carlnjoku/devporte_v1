from flask import request
from flask_restplus import Resource

from ..utils.decorator import token_required

from ..model.userDto import UserDto


from app.main.service.user_services import (get_all_users, get_a_user, 
                                            signup, update_profile, do_email_confirmation, 
                                            get_user_minimal_info, get_skills, get_an_employer_intro,
                                            update_employer_contact, change_password
                                            )
                                      
from app.main.service.sendemail_service import send_email_confirmation



api = UserDto.api
_user = UserDto.signup
_profile = UserDto.profile
_email_confirmation = UserDto.email_confirmation
_fileupload = UserDto.fileupload
_emp_contact = UserDto.emp_contact
_change_pass = UserDto.change_pass

upload_parser = UserDto.upload_parser

parser = UserDto.parser



@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()
   
    
    @api.response(201, 'User successfully created !')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return signup(data=data)

@api.route('/check_user_status/<user_type>')
class CheckStatus(Resource):
    #@api.expect(parser)
    @token_required
    def get(self, current_user, user_type):
        # get auth token
        print(current_user)
        return get_a_user()

@api.route('/send_email_confirmation')
class EmailConfirmation(Resource):
    @api.response(201, 'Confirmation email sent !')
    @api.doc('email confirmation')
    @api.expect(_email_confirmation, validate=True)
    def post(self):
        """Email confirmation """
        data = request.json
        return send_email_confirmation(data=data)

@api.route('/update_email_confirmation/<_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class UpdateEmailConfirmation(Resource):
    @api.doc('Update a user email confirmation')
    #@api.marshal_with(_user)
    def get(self, _id):
        """Update email confirmation with its identifier"""
        user = do_email_confirmation(_id)
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/update_profile')
class ProfileUpdate(Resource):
    @api.response(201, 'Profile updated successfully')
    @api.doc('Initial profile update')
    @api.expect(upload_parser, validate=True)

    def put(self):
        """ Update minimal profile """
        
        args = upload_parser.parse_args() # upload a file
        uploaded_file = args['avatarBlob']
        req_data = request.form.to_dict(flat=True)

        return update_profile(req_data, uploaded_file)

@api.route('/<userId>')
@api.param('userId', 'The User identifier')
@api.response(404, 'User not found.')

class User(Resource):
    @api.doc('get a user')
    #@api.marshal_with(_user, envelope='data')
    def get(self, userId):
        """get a user given its identifier"""
        return get_a_user(userId)

@api.route('/intro/<empId>')
@api.param('userId', 'The User identifier')
@api.response(404, 'User not found.')

class EmployerIntro(Resource):
    @api.doc('get an employer intro')
    #@api.marshal_with(_user, envelope='data')
    def get(self, empId):
        """get a user given its identifier"""
        return get_an_employer_intro(empId)     

@api.route('/check_for_authorization/<user_type>')
@api.param('user_type', 'The User type')
@api.response(401, 'Unauthorized.')
class CheckUser(Resource):
    @token_required
    @api.doc('check user authorization before login')
    #@api.marshal_list_with(_user, envelope='data')
    def get(self, current_user, user_type):
        #user_type = 'employer'
        return get_loggedin_user(user_type)


@api.route('/change_password')
class PaswordChange(Resource):
    @api.response(201, 'Password changed successfully !')
    @api.doc('Change password')
    @api.expect(_change_pass, validate=True)
    def post(self):
        """Change user password """
        data = request.json
        return change_password(data=data)

@api.route('/tools')
class SkillList(Resource):
    @api.doc('list_of_skills')
    #@api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_skills()


########################
# EMPLOYER             #
########################

@api.route('/update_employer_contact')
class UpdateEmployerContact(Resource):
    @api.response(201, 'Contact updated successfully')
    @api.doc('Employer contact update')
    @api.expect(_emp_contact, validate=True)

    def put(self):
        """ Update employer's contact """
        data = request.json
        return update_employer_contact(data=data)






