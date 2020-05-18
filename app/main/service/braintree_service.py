from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import json

from app.main import mongo
from bson.objectid import ObjectId

from ..config import gateway



##################
# CUSTOMER       #
##################

def create_customer(data):
    try:
        # Check if customer exist
        check_customer = mongo.db.customers.find_one({'employerId':data['employerId']})
        if check_customer is None:

            # Create a new customer_id 
            cust_data = {
              "first_name": data['first_name'],
              "last_name": data['last_name'],
              "email": data['email'],
              "company": data['company'],
            }
            result = gateway.customer.create(cust_data)

            #result.is_success
            # True

            #result.customer.id
            # e.g. 594019
            
            # insert new customer details in transaction collection on devporte db

            data['_id'] = result.customer.id
            mongo.db.customers.insert_one(data)

            return jsonify({"data": result.customer.id})
        else:
            custId = mongo.db.customers.find_one({'employerId':data['employerId']}, {'_id':1})
            cId = custId['_id']
            return jsonify({"data": cId})
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})

def create_customer_with_payment(data):
    try:
        # Check if customer exist
        check_customer = mongo.db.customers.find_one({'employerId':data['employerId']})
        if check_customer is None:

            # Create a new customer_id 
            cust_data = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email'],
                "company": data['company'],
            }
            
            result = gateway.customer.create(cust_data)

            data['_id'] = result.customer.id
            mongo.db.customers.insert_one(data)

            response_object = {
                'status': result.is_success,
                'data': result.customer.id
            }

            #result.is_success
            # True

            #result.customer.id
            # e.g 160923

            result.customer.payment_methods[0].token
            # e.g f28w
        else:
            
            custId = mongo.db.customers.find_one({'employerId':data['employerId']}, {'_id':1})
            cId = custId['_id']
            return jsonify({"data": cId})

    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})


def update_customer(data):
    try:
        check_customer = mongo.db.customers.find_one({'_id':data['customerId']})
        print(check_customer)
        if check_customer is not None:
            cust_data = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email'],
                "company": data['company'],
            }

            result = gateway.customer.update(data['customerId'], cust_data) 
            

            mongo.db.customers.update_one({"_id":data['customerId']}, {"$set":data}, upsert=True)
            response_object = {
                'status': 'success',
                'data': 'Customer successfully updated'
            }

            return response_object, 200

        else:
            
            response_object = {
                'status': 'fail',
                'data': 'Customer does not exist'
            }
            return response_object, 401

    except Exception as e:

            response_object = {
                'status': 'fail',
                'data': 'Something went wrong, try again'
            }
            return response_object, 501

def get_customer(customerId):
    try:
        #customer = gateway.customer.find(customerId)
        customer = mongo.db.customers.find_one({"_id":customerId})
        response_object = {
            'status': 'success',
            'data': customer
        }

        return response_object, 200

    except Exception as e:
        response_object = {
            'status': 'fail',
            'data': 'Something went wrong, try again'
        }
        return response_object, 501

def delete_customer(customerId):
    try:

        result = gateway.customer.delete(customerId)
        if result:
            mongo.db.customers.remove({"customerId":customerId})
            # True
            response_object = {
                    'status': 'success',
                    'data': result.is_success
                }
            return response_object, 200
        else:
            response_object = {
                    'status': 'faill',
                    'data': 'Customer does not exist'
                }
            return response_object, 401


    except Exception as e:
        
        response_object = {
            'status': 'fail',
            'data': 'Something went wrong, try again'
        }
        return response_object, 501



#########################
# Payment Method Nonces # 
#########################

# A payment method nonce is a secure, one-time-use reference to payment information. 
# It's the key element that allows your server to communicate sensitive payment 
# information to Braintree without ever touching the raw data.
# Any type of payment method can be referenced by a payment method nonce.

def generate_token(empId):
    try:
        client_token = gateway.client_token.generate({
            "customer_id": empId
        })
        #generate nouce
        #print(client_token)
        return  jsonify({"data":client_token})
    except Exception as e:
        
        return jsonify({"data":e}), 500  


##################
# PAYMENT METHOD #
##################


def get_payment_method(token):
    try:
        paymethod = gateway.payment_method.find(token)
       
        details = paymethod
        payment_method_details = {
            'bin': details.bin,
            'card_type': details.card_type,
            'cardholder_name': details.cardholder_name,
            'customer_id': details.customer_id,
            'debit': details.debit,
            'default': details.default,
            'expiration_month': details.expiration_month,
            'expiration_year': details.expiration_year,
            'expired': details.expired,
            'image_url': details.image_url,
            'issuing_bank': details.issuing_bank,
            'last_4': details.last_4,
            'token': details.token,
       
        }
    
        response_object = {
            'status':'success',
            'data': payment_method_details
        }
        return response_object, 201 

    except Exception as e:
        response_object = {
        'status':'fail',
        'data': e
    }
    
    

def create_payment_method(data):
    try:
        # Check if payment method already exists
        check_payment_method_exist = mongo.db.payment_methods.find_one({"make_default": { '$exists': True }})
        
        print(check_payment_method_exist)

        if check_payment_method_exist is not None:
            req_data = {
                "payment_method_nonce":data['payment_method_nonce'], 
                "customer_id": data['customer_id'],
                "options": {
                    "fail_on_duplicate_payment_method": True,
                    "verify_card": True,

                }
            }

            
            
            result = gateway.payment_method.create(req_data)
            details = result.payment_method
            print(details + "yes")
            
            payment_method_details = {
                'employerId' : data['employerId'],
                'bin': details.bin,
                'card_type': details.card_type,
                'cardholder_name': details.cardholder_name,
                'commercial': details.commercial,
                'country_of_issuance': details.country_of_issuance,
                'created_at': details.created_at,
                'customer_id': details.customer_id,
                'customer_global_id': details.customer_global_id,
                'customer_location': details.customer_location,
                'debit': details.debit,
                'default': details.default,
                'expiration_month': details.expiration_month,
                'expiration_year': details.expiration_year,
                'expired': details.expired,
                'global_id': details.global_id,
                'graphql_id': details.graphql_id,
                'healthcare': details.healthcare,
                'image_url': details.image_url,
                'issuing_bank': details.issuing_bank,
                'last_4': details.last_4,
                'token': details.token,
                'updated_at': details.updated_at,
                'venmo_sdk': details.venmo_sdk,
                'verifications': []
            }
            
            payment_method_details['_id'] = str(ObjectId())
            mongo.db.payment_methods.insert_one(payment_method_details)
            response_object = {
                'status': 'success',
                'data': 'Payment method added successfully'
            }
            return response_object, 201

        else:
            req_data = {
                "payment_method_nonce":data['payment_method_nonce'], 
                "customer_id": data['customer_id'],
                "options": {
                    "make_default": True,
                    "fail_on_duplicate_payment_method": True,
                    "verify_card": True
                }
            }

            
            print(req_data)
            result = gateway.payment_method.create(req_data)
            print(result)
            details = result.payment_method
            print(details)
            
            payment_method_details = {
                'employerId' : data['employerId'],
                'bin': details.bin,
                'card_type': details.card_type,
                'cardholder_name': details.cardholder_name,
                'commercial': details.commercial,
                'country_of_issuance': details.country_of_issuance,
                'created_at': details.created_at,
                'customer_id': details.customer_id,
                'customer_global_id': details.customer_global_id,
                'customer_location': details.customer_location,
                'debit': details.debit,
                'default': details.default,
                'expiration_month': details.expiration_month,
                'expiration_year': details.expiration_year,
                'expired': details.expired,
                'global_id': details.global_id,
                'graphql_id': details.graphql_id,
                'healthcare': details.healthcare,
                'image_url': details.image_url,
                'issuing_bank': details.issuing_bank,
                'last_4': details.last_4,
                'token': details.token,
                'updated_at': details.updated_at,
                'venmo_sdk': details.venmo_sdk,
                "make_default": True,
                'verifications': []
            }
            
            payment_method_details['_id'] = str(ObjectId())
            mongo.db.payment_methods.insert_one(payment_method_details)
            
            response_object = {
                'status': 'success',
                'data': 'Payment method added successfully'
            }

            return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'data': dict(e)
        }

        return response_object, 501


def update_payment_method():
    try:
        result = gateway.payment_method.update("the_token", {
            "billing_address": {
                "street_address": "100 Maple Lane",
                "options": {
                    "update_existing": True
                }
            }
        })

    except Exception as e:
        response_object = {
            'status': 'fail',
            'data': e
        }

        return response_object, 501


def delete_payment_method(token):
    print(token)
    result = gateway.payment_method.delete(token)
    print(result)
    result.is_success
    # True

    return result.is_sucess


def get_user_list_payment_methods(empId):
    print(empId)
    pms = mongo.db.payment_methods.find({"employerId":empId}, {"created_at":0, "updated_at":0})
    response_object = {
            'status':'success',
            'data': list(pms)
        }
    print(list(pms))
    return response_object, 201


def get_primary_card(employerId):
    
    payment_method = mongo.db.payment_methods.find({'employerId':employerId, 'primary_card':True})

    print(payment_method)
    if payment_method is not None:
        
        response_object = {
                'status': 'success',
                'data': dict(payment_method)
            }
        print(response_object)
        return response_object, 201
    else:

        response_object = {
                'status': 'success',
                'data': 'No payment method found'
            }

        return response_object, 401



##################
# TRANSACTIONS   #
##################

def pay():
    try:
        req_data = request.get_json()
         
        amount = int(req_data['amount'])
        nonce_from_the_client = req_data['nonce_from_the_client']
        customerId = req_data['customerId']
        employerId = req_data['employerId']
        projectId = req_data['projectId']
        created_on = req_data['created_on']

        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce_from_the_client,
            #"device_data": device_data_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            # See result.transaction for details
            transactionId = result.transaction.id
            msg = result.transaction.processor_response_text
            
            # Insert transaction collection to the database
            tranctData = {
                'transactionId': transactionId,
                'customerId': customerId,
                'employerId': employerId,
                'projectId': projectId,
                'amount': amount,
                'created_on': created_on
            }
            

            tracn = mongo.db.transactions.insert_one(tranctData)

            #Update employer by adding deposit 
            y = mongo.db.users.update_one({ '_id': employerId}, {'$inc': {'deposit': amount}})
            print(y)            
                        
            response = {
                'transactionId': transactionId,
                'msg': msg
            }
            return jsonify({"data":response})
        else:
            # Handle errors
            for error in result.errors.deep_errors:
                print("attribute: " + error.attribute)
                print("code: " + error.code)
                print("message: " + error.message)
            return jsonify({"data: " + error.message})
    except Exception as e:
        return jsonify({"result":{"error_msg": str(e)}})


"""
        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce_from_the_client,
            #"device_data": device_data_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })

"""