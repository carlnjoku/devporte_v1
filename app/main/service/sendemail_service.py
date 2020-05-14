from flask import Flask, request, jsonify, make_response, render_template
import uuid
import datetime

from app.main import mongo
from bson.objectid import ObjectId

from ..config import key

from app.main import sendemail
from flask_mail import Message



def send_email_confirmation(data):

    firstname = data['firstname']
    lastname = data['lastname']
    fullname = data['firstname']+ ' ' +data['lastname']
    userId = data['_id']
    message_body = "Verify your email address to complete registration  Hi Chinedu,Thanks for your interest in joining Upwork! To complete your registration, we need you to verify your email address.Verify Email Please note that not all applications to join Upwork are accepted. We will notify you of our decision by email within 24 hours.Thanks for your time,The Upwork Team"
    subject = "Email confirmation"
    msg = Message(
        subject, 
        recipients=['flavoursoft@yahoo.com', 'flavoursoft@gmail.com'], 
        body = 'Hello '+fullname+',\nYou or someone else has requested that a new password be generated for your account. If you made this request, then please follow this link:',
        html = render_template(
            './signup.html', 
            firstname=firstname, 
            message_body=message_body,
            userId = userId
        ),
        sender=['Devporte', 'signup-noreply@devporte.com']
    )
    sendemail.send(msg)
    response_object = {
                'status': 'success',
                'data': 'Confirmation email sent'
            }
    return response_object
   