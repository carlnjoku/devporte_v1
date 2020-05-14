import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']



import pyrebase

import braintree

import hyperwallet

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devporte_secret_key')
    DEBUG = False

    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="qgc7sgct9mnbmpx5",
        public_key="mbm6gsqbp8znnn8s",
        private_key="a0a13d2f534b7999d18cb55272e0abb1"
        )
    )

    hyper = hyperwallet.Api(
        "restapiuser@39011931613",
        "angel@4340",
        "prg-bbfd3080-0a52-4802-8e7c-869f72518955",
        "https://api.sandbox.hyperwallet.com/rest/v3/users"  
    )


    config = {
        
        "apiKey": "AIzaSyAIQcCsIQk3i-uIFnPnINhs6F3PJa3H418",
        "authDomain": "devporte-64919.firebaseapp.com",
        "databaseURL": "https://devporte-64919.firebaseio.com",
        "projectId": "devporte-64919",
        "storageBucket": "devporte-64919.appspot.com",
        "messagingSenderId": "943749828225",
        "appId": "1:943749828225:web:3f65bee5527a2d27098780",
        "measurementId": "G-5HH7B19XJJ"
    
    }

    firebase = pyrebase.initialize_app(config)

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    db_name = 'devporte'
    db_host_mongo = '0.0.0.0'
    db_port_mongo = '27017'
    MONGO_URI = "mongodb://{db_host}:{db_port_mongo}/{db_name}".format(
    #username=username, password=password, db_host=db_host_mongo,
    db_host=db_host_mongo,
    db_port_mongo=db_port_mongo, db_name=db_name)
    
    MAIL_SERVER = 'mail.devporte.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    #Gmail SMTP port (TLS): 587.
    #SMTP port (SSL): 465.
    #SMTP TLS/SSL required: yes.
    MAIL_USERNAME = 'info@devporte.com'
    MAIL_PASSWORD = 'angel4340'


class TestingConfig(Config):
    DEBUG = True
    TESTING = False
    db_name = 'devporte'
    db_host_mongo = '0.0.0.0'
    db_port_mongo = '27017'
    MONGO_URI = "mongodb://{db_host}:{db_port_mongo}/{db_name}".format(
    #username=username, password=password, db_host=db_host_mongo,
    db_host=db_host_mongo,
    db_port_mongo=db_port_mongo, db_name=db_name)
    

    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    #PRESERVE_CONTEXT_ON_EXCEPTION = False
    #SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    db_name = 'devporte'
    db_host_mongo = '0.0.0.0'
    db_port_mongo = '27017'
    MONGO_URI = "mongodb://{db_host}:{db_port_mongo}/{db_name}".format(
    #username=username, password=password, db_host=db_host_mongo,
    db_host=db_host_mongo,
    db_port_mongo=db_port_mongo, db_name=db_name)

    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
gateway = Config.gateway
firebase = Config.firebase


