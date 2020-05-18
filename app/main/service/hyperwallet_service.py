from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import json

from app.main import mongo
from bson.objectid import ObjectId

import pycurl
from urllib.parse import urlencode
from io import StringIO

from ..config import hyperwallet



def create_user():
    try:
        #req_data = request.get_json()
        data = {
            "clientUserId": request.form['clientUserId'],
            "profileType": request.form['profileType'],
            "firstName": request.form['firstName'],
            "lastName": request.form['lastName'],
            "email": request.form['email'],
            #"stateProvince": request.form['stateProvince'],
            "country": "NG",
            "postalCode": request.form['postalCode'],
            "programToken": "prg-15dc9c13-04b0-4bca-9bd4-80495b25a8ef",

        }

    
        response = hyperwallet.createUser(data)

        # Get user token 
        token = response.token

        # Create payee account
        data['_id'] = str(ObjectId())
        data['payeeToken'] = token
        mongo.db.payee.insert_one(data)

        
        #Update user's collection
        mongo.db.payee.users.update_one({'_id':request.form['clientUserId']}, {'$set':{'payeeToken':token}})
        
        #print(response)
        return jsonify({"data": token})

    except Exception as e:
        return jsonify({"data":{"error_msg":str(e)}})



# List users
def list_users():
    response = hyperwallet.listUsers()
    print(response)

    #return response
    return jsonify({"data": "hello"})


# Update user
def update_user():
    data = {
        "firstName": "John",
        "lastName": "Smith",
        "email": "j@email.com"
    }
    response = hyperwallet.updateUser("usr-f9154016-94e8-4686-a840-075688ac07b5", data)



#Delete user
def retrieve_user():
   # userToken = request.args.get('usr-07954d75-2f4f-4f76-af96-4c42d1b4da71') 
    response = hyperwallet.getUser('usr-07954d75-2f4f-4f76-af96-4c42d1b4da71')
    print(response)
    return jsonify({"data":"done"})


# Get payee details from devporte database
def get_payee():
    try:
        payeeToken = request.args.get('token') 
        user = mongo.db.payee.find_one({"payeeToken":payeeToken})

        return jsonify({"data": user})
    
    except Exception as e:
        return jsonify({"data":{"error_msg":str(e)}})


# Create bank 
def create_bank():
    try:
        payeeToken = request.form['token']
        userId = request.form['userId']
        
        data = {
            "profileType": request.form["profileType"],
            "transferMethodCountry": request.form["transferMethodCountry"],
            "transferMethodCurrency": request.form["transferMethodCurrency"],
            "type": request.form["type"],
            "branchId": request.form["branchId"],
            "bankAccountId": request.form["bankAccountId"],
            "bankAccountPurpose": request.form["bankAccountPurpose"],
            "firstName": request.form["firstName"],
            "lastName": request.form["lastName"],
            "country": request.form["country"],
            "stateProvince": request.form["stateProvince"],
            "addressLine1": request.form["addressLine1"],
            "city": request.form["city"],
            "postalCode": request.form["postalCode"],
            "bankAccountRelationship": "SELF"
        }

        
        response = hyperwallet.createBankAccount(payeeToken, data)

        # Get bank token
        token = response.token

        if token is not None:

            data['_id'] = str(ObjectId())
            data['payMethodToken'] = token
            data['userId'] = userId
            method = database['paymethods'].insert_one(data)

        return jsonify({"data":token})
    
    except Exception as e:
        return jsonify({"data":{"error_msg":str(e)}}) 




def retrieve_bank():
    response = hyperwallet.getBankAccount("usr-c4292f1a-866f-4310-a289-b916853939de", "trm-56b976c5-26b2-42fa-87cf-14b3366673c6");


def update_bank():
    data = {
        "bankAccountId": 7861012345
    }
    response = hyperwallet.updateBankAccount("usr-c4292f1a-866f-4310-a289-b916853939de", "trm-56b976c5-26b2-42fa-87cf-14b3366673c6", data);


def list_banks():
    response = hyperwallet.listBankAccounts("usr-c4292f1a-866f-4310-a289-b916853939de")



def create_bank_card():
    try:
        payeeToken = request.form['token']
        url = 'https://api.sandbox.hyperwallet.com/rest/v3/users/'+payeeToken+'/bank-cards'

        data = {'field': 'value'}
        pf = urlencode(data)


        response = StringIO.StringIO()

        c = pycurl.curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDSIZE, 0)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, 
            ['Accept:application/json',
            'X-Requested-By:MyClient',
            'Content-Type:',
            'Content-Length:'])
        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.USERPWD, "user:pass")
        c.perform()

    except Exception as e:
        return jsonify({"data":{"error_msg":str(e)}}) 



def create_paypal():
    try:

        payeeToken = request.form['token']
        userId = request.form['userId']

        print(payeeToken)
        data = {
            "type": request.form['type'],
            "transferMethodCountry": request.form['transferMethodCountry'],
            "transferMethodCurrency": request.form['transferMethodCurrency'],
            "email": request.form['email']
        }
    
        
        response = hyperwallet.createPayPalAccount(payeeToken, data)
        
        token = response.token
        print(response)
        if token is not None:

            data['_id'] = str(ObjectId())
            data['payMethodToken'] = token
            data['userId'] = userId
            method = mongo.db.paymethods.insert_one(data)

        return jsonify({"data":token})
        
    except Exception as e:
        return jsonify({"result":{"error_msg":str(e)}})
    

# Get payee details from devporte database

def get_payment_method():
    try:
        userId = request.args.get('userId') 
        print(userId)
        payTypes = mongo.db.paymethods.find({"userId": userId})

        return jsonify({"data": list(payTypes)})
    
    except Exception as e:
        return jsonify({"data":{"error_msg":str(e)}})
