from flask import request
from flask_restplus import Resource

from ..model.financeDto import FinanceDto
from app.main.service.finance_service import (get_a_project_by_empId, 
                                              get_a_project, get_a_project_by_titleId, 
                                              update_a_project
                                             )
from app.main.service.braintree_service import (get_payment_method, create_payment_method, generate_token, 
                                                create_customer, update_customer, get_user_list_payment_methods,
                                                get_primary_card, get_customer, delete_customer, delete_payment_method
                                            
                                             )

from app.main.service.sendemail_service import send_email_confirmation


from app.main.service.hyperwallet_service import (create_user)

api = FinanceDto.api
_customer = FinanceDto.customer
_payment_method = FinanceDto.payment_method
_customer_update = FinanceDto.customer_update



@api.route('/payment_method/<token>')
@api.param('token', 'Customer token')
class GetPaymentMethod(Resource):
    @api.doc('Get payment method')
    def get(self, token):
        """Get payment methods its customer token"""
        return get_payment_method(token)   

@api.route('/create_payment_method')
class PaymentMethodNew(Resource):
    @api.response(201, 'Payment method successfully created !')
    @api.doc('Create a new payment method')
    @api.expect(_payment_method, validate=True)
    def post(self):
        """Create a new payment method """
        data = request.json
        return create_payment_method(data=data) 


@api.route('/<employerId>')
class ListCustomerPaymentMethods(Resource):
    @api.doc('list_of_user_payment_methods')
    def get(self, employerId):
        """List all customer's payment_methods"""
        return get_user_list_payment_methods(employerId)

@api.route('/primary_card/<employerId>')
class PrimaryCard(Resource):
    @api.doc('Get primary payment method with employerId')
    def get(self, employerId):
        """Get primary payment method"""
        return get_primary_card(employerId)

@api.route('/delete_payment_method/<token>')
class DeletePayMethod(Resource):
    @api.doc('Delete payment method with token')
    def delete(self, token):
        """Delete payment method"""
        return delete_payment_method(token)
           

@api.route('/')   
class CreateCustomer(Resource):   
    @api.response(201, 'Customer successfully created !')
    @api.doc('Create customer')
    @api.expect(_customer, validate=True)
    def post(self):
        """Create a new customer """
        data = request.json
        return create_customer(data=data)

    @api.response(201, 'Customer successfully updated !')
    @api.doc('Update Customer')
    @api.expect(_customer_update, validate=True)
    def put(self):
        """Update a Customer """
        data = request.json
        return update_customer(data=data)


@api.route('/get_customer/<customerId>')   
class GetCustomer(Resource):   
    @api.doc('Get customer')
    def get(self, customerId):
        """Get a single customer """
        return get_customer(customerId)

@api.route('/delete_customer/<customerId>')   
class DeleteCustomer(Resource):   
    @api.doc('Delete customer')
    def delete(self, customerId):
        """Delete a single customer """
        return delete_customer(customerId)

    

@api.route('/generate_token/<customerId>')
@api.param('empId', 'Generate token with customerId identifier')
@api.response(404, 'User not found.')
class GetToken(Resource):
    @api.doc('Generate token to create a transaction')
    def get(self, customerId):
        """Generate token with its identifier"""
        return generate_token(customerId)
       

    

"""
{
  "first_name": "Carl",
  "last_name": "Njoku",
  "email": "sudo@flavoursoft.com",
  "company": "Flavoursoft Consulting Limited",
  "customerId": "886390541"
}
"""

###############
# HYPERWALLET #
###############


# Create user 
create_user