from flask import Flask, request, jsonify
from flask import request
from flask_restplus import Resource
from app.main import mongo
from flask_socketio import emit, send, join_room
from app.main import socketio
from app.main.service.socketio_service import save_message, save_project_feeds
from bson.objectid import ObjectId



from flask import Blueprint


api = Blueprint('socket', __name__)

@api.route('/')

@socketio.on('message')
def connect(data):
    print(data)
    x = mongo.db.users.update({'_id':data}, {'$set':{'online':True}})
    join_room(data)
    response = 'true'
    emit('connected', response, broadcast=True)
    print(response)

@socketio.on('disconnect', namespace='/private')
def disconnect(data):
    x = mongo.db.users.update({'_id':data}, {'$set':{'online':False}})
    response = 'false'
    emit('user_disconnected_annoucement', response)
    print(data)
    disconnect(request.sid, namespace='/private')
    print(request.sid+ 'yep')


# user enters the room 
@socketio.on('message1', namespace='/private')
def message(data):
    join_room(data['room'])
    emit('join_room_annoucement', data, broadcast=True)
    print('Carlo' + data['room'])

@socketio.on('disconnect1', namespace='/private')
def disconnect():
    
    emit('disconnect_anouncement', 'disconneted', broadcast=True)
    print('disconnected')

# proposal notification
@socketio.on('proposal_notification', namespace='/private')
def manage_notification(data):
    join_room(data['room'])
    emit('proposal_notification_annoucement', data, room=data['room'])
    print(data)


@socketio.on('send_message', namespace='/private')
def handle_send_message(payload):
    message_body = payload['message_body']
    room = payload['room']
    senderId = payload['senderId']
    created_on = payload['created_on']
    recepientId = payload['recepientId']
    recepient_avatar = payload['recepient_avatar']
    recepient_fname = payload['recepient_fname']
    recepient_lname = payload['recepient_lname']
    recepient_email = payload['recepient_email']
    senderId =  payload['senderId']
    sender_fname =  payload['sender_fname']
    sender_lname = payload['sender_lname']
    sender_email = payload['sender_email']
    sender_avatar = payload['sender_avatar']
    
    print('my room' + room)
    #Save message
    save_message(room, message_body, senderId, created_on, recepientId, recepient_avatar, recepient_fname, 
    recepient_lname, recepient_email, sender_fname, sender_lname, sender_email, sender_avatar )
    print(payload)
    
    emit('new_message', {'message':message_body, 'sender_avatar':sender_avatar, 'sender_fname':sender_fname, 'sender_lname':sender_fname, 'created_on':created_on}, room=room)

@socketio.on('typing',  namespace='/private' )
def handle_typing(data):
    emit('start_typing', data, broadcast=True)
    #print(data['message'])

@socketio.on('new_job_post')
def handle_new_job_post(payload):
    
    #room = '5e47e537c1f8d023941a76c5'
    #employerId = payload['employerId']
    projectId = payload['projectId']
    project_type = payload['project_type']
    expertise = payload['expertise']
    experience_level = payload['experience_level']
    created_on = payload['created_on'],
    
    print(project_type)

    #print('files' +file)
    
    #Check if file is submitted
    #if len(file) > 0:
        #uploaded_files = upload_files(file)

    #print(uploaded_files)
    #Save project post 
    #projectId = save_project(employerId, employer_name, firstname, lastname, email, title, job_description, project_type, expertise, experience_level, payment_type, project_time, file, status, initial_route, created_on)

    #print('ProjectId: '+ projectId)
    
    #Match jobs with freelancers

   #Match jobs with freelancers
    users = mongo.db.users.aggregate([
        {
            "$match":{'primary_skills': { '$elemMatch': {'tool_name' : 'Python', 'tool_name': 'React Js', 'tool_name' : 'Java'}}},
            
        },
        {
            "$project": {"_id":0, "firstname":1, "lastname":1}
        }
        
    ])

    users = list(users)
    
    #print(list(users))
    for user in users:
        #print(user['_id'])
        msg = {'userId':user['_id'], 'jobTitile':payload['title'] }
        feed = {'_id': str(ObjectId()), 'userId':user['_id'], 'projectId': projectId, 'created_on':created_on }

        # Insert into project feeds
        save_project_feeds(feed)
        emit('new_job_post_announcement', msg, room=user['_id'])

