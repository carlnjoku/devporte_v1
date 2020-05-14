from flask import Flask, request, jsonify
from app.main import mongo
from bson.objectid import ObjectId


def add_room(room, employerId, developerId, created_on, room_members_data, firstname, lastname, avatar,  project_title):
    room_id = mongo.db.rooms.insert({'_id':str(ObjectId()), 'room':room, 'employerId': employerId, 'developerId': developerId, 'created_on':created_on, 'firstname':firstname, 'lastname':lastname, 'avatar':avatar, 'project_title':project_title })
    print('hey' + room_id )
    add_room_members(room_id, room, room_members_data)
    return room_id

# Add single room member
def add_room_member(room_id, room, projectId, project_title, userId, avatar, firstname, lastname, email, created_on, isRoomAdmin=False):
    mongo.db.room_members.insert_one({'room_id':room_id, 'room':room, 'project_title':project_title, 'userId':userId, 'avatar': avatar,  'firstname': firstname, 'lastname': lastname, 'email':email, 'created_on': created_on, 'isRoomAdmin':isRoomAdmin, })

# Add multiple room members
def add_room_members(room_id,room, room_members_data): 
    #print(room_members_data)
    #Update incoming member data by adding room_id and room to member_data
    room_members_data[0].update(room = room, room_id = room_id)
    room_members_data[1].update(room = room, room_id = room_id)
   
    
    mongo.db.room_members.insert_many(room_members_data)

def save_message(room, message_body, senderId, created_on, recepientId, recepient_avatar, recepient_fname, recepient_lname, recepient_email, sender_fname, sender_lname, sender_email, sender_avatar):
    message = mongo.db.messages_collection.insert_one({'room':room, 'message_body': message_body, 'senderId':senderId, 'created_on':created_on, 'recepientId': recepientId, 'recepient_avatar':recepient_avatar, 'recepient_fname':recepient_fname, 'recepient_lname':recepient_lname, 'recepient_email':recepient_email,
    'sender_fname':sender_fname, 'sender_lname':sender_lname, 'sender_email':sender_email, 'sender_avatar':sender_avatar})
    
def get_messages(room_id):
    return list(mongo.db.messages_collection.find({'room_id':room_id}))

def send_notification(expertise, experience_level):
    pipeline = { 'primary_skills':expertise, 'experience_level':experience_level }
    #users = users_collection.aggregate([{"$match":pipeline}])
    #print(expertise)
    #print(list(users))
    #return list(users)

    #pipeline = { 'pri':expertise, 'experience_level':experience_level }

    #[{"$match": {'primary_skills':{'title': '12 Angry Men', 'year': 1957}, 'experience_Level' : 'intermediate' } }]
    users = mongo.db.users_collection.aggregate([{"$match":{ 'primary_skills': {'title': '12 Angry Men', 'year': 1957}, 'experience_level':'intermediate' }}])
    #return jsonify({"msg": "Job successfully created!!!"})
    #print('you')
    return (users)

#def save_project(employerId, employer_name, firstname, lastname, email, title, job_description, project_type, expertise, experience_level, payment_type, project_time, status, initial_route, upload_files, created_on):
    #projectId = project_collection.insert_one({'_id': str(ObjectId()), 'employerId':employerId, 'employer_name':employer_name, 'firstname':firstname, 'lastname':lastname, 'email':email, 'title':title, 'job_description':job_description, 'project_type':project_type, 'expertise':expertise, 'experience_level':experience_level, 'payment_type':payment_type, 'project_time':project_time, 'project_files':upload_files, 'status':status, 'initial_route': initial_route, 'created_on':created_on}).inserted_id
    
    #return (projectId)
    

def save_project_feeds(feed):
    feed = mongo.db.project_feeds_colection.insert_one(feed)

def update_project(projectId, bid):
    print(projectId)
    mongo.db.jobs.update_one({'projectId':projectId}, {'$addToSet':{'bid':int(bid)}})

