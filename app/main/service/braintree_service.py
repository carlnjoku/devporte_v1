from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import json

from app.main import mongo
from bson.objectid import ObjectId

from ..config import gateway



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

def update_customer():
    pass    

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
        req_data = {
            "payment_method_nonce":data['payment_method_nonce'], 
            "customer_id": data['customer_id'],
        }
        
        result = gateway.payment_method.create(req_data)
        details = result.payment_method
        
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
    except Exception as e:
        response_object = {
            'status': 'fail',
            'data': e
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

def generate_token(empId):
    try:
        client_token = gateway.client_token.generate({
            "customer_id": empId
        })
        print(client_token)
        #generate nouce

        #print(client_token)
        return  jsonify({"data":client_token})
    except Exception as e:
        
        return jsonify({"data":e}), 500  


def get_user_list_payment_methods(empId):
    pms = mongo.db.payment_methods.find({"employerId":empId})
    response_object = {
            'status':'success',
            'data': list(pms)
        }
    return response_object, 201
