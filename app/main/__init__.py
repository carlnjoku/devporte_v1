from flask import Flask
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

from .config import config_by_name
from flask_mail import Mail, Message
from flask_socketio import SocketIO
from flask_cors import CORS

#db = SQLAlchemy()
mongo = PyMongo()
flask_bcrypt = Bcrypt()
sendemail = Mail()
socketio = SocketIO()




def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    mongo.init_app(app)
    sendemail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    

    


    
    
    flask_bcrypt.init_app(app)

    return app
