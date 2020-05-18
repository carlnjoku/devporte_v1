from flask_restplus import Namespace, fields


class FinanceDto:
    api = Namespace('customer', description='Customer related operations')
    customer = api.model('customer_details', {
        'first_name': fields.String(required=True, description='user email address'),
        'last_name': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user password'),
        'company': fields.String(required=True, description='user password'),
        'employerId': fields.String(required=True, description='user password')

    })

    customer_update = api.model('update customer_details', {
        'first_name': fields.String(required=True, description='user email address'),
        'last_name': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user password'),
        'company': fields.String(required=True, description='user password'),
        'customerId': fields.String(required=True, description='user password')

    })



    payment_method = api.model('payment method', {
        'customer_id': fields.String(required=True, description='customer id'),
        'payment_method_nonce': fields.String(required=True, description='payment method nonce'),
        'employerId': fields.String(required=True, description='employerId'),

    })
    """
    payment_method_response = api.model('payment method response', {
        'bin': fields.String(required=True, description='customer id'),
        'card_type': fields.String(required=True, description='customer id'),
        'cardholder_name': fields.String(required=True, description='customer id'),
        'customer_id': fields.String(required=True, description='customer id'),
        'debit': fields.String(required=True, description='customer id'),
        'default': fields.String(required=True, description='customer id'),
        'expiration_month': fields.String(required=True, description='customer id'),
        'expiration_year': fields.String(required=True, description='customer id'),
        'expired': fields.String(required=True, description='customer id'),
        'image_url': fields.String(required=True, description='customer id'),
        'issuing_bank': fields.String(required=True, description='customer id'),
        'last_4': fields.String(required=True, description='customer id'),
        'token': fields.String(required=True, description='customer id'),
    })

    """
