from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import json

from app.main import mongo
from bson.objectid import ObjectId

from app.main.service.socketio_service import update_project, add_room
from app.main.service.braintree_service import create_customer
from app.main.utils.file_upload import upload_multiple_files


def new_project(data, upload):
    
    data['projectId'] = str(uuid.uuid4())
    data['_id'] = str(ObjectId())
    projectId = mongo.db.jobs.insert_one(data).inserted_id

    if projectId is not None:
        # insert uploaded file links to project files collection
        filenames =  upload_multiple_files(upload) # Get uploaded file or files
      
        if len(filenames) is not None :
            # create file collection for this project
            mongo.db.files.insert_one({"_id":str(ObjectId()), "projectId":projectId, "files":filenames})
        
            response_object = {
                "status":"success",
                "message": projectId
            }
            return response_object, 201

    else:
        response_object = {
            "status":"success",
            "message": "Error occured posting the project. Try again"
        }
        return response_object, 404    



def get_a_project_projectId(projectId):
    try:
        project = mongo.db.jobs.find_one({"projectId": projectId})
        if project is not None:
            response_object = {
                "status":"success",
                "message": project
            }
            return response_object, 201
        else:
            
            response_object = {
                "status":"fail",
                "message": "Project not found"
            }
            return response_object, 404
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})

def get_a_project_titleId(titleId):
    try:
        project = mongo.db.jobs.find_one({"titleId": titleId})
        if project is not None:
            response_object = {
                "status":"success",
                "data": project
            }
            return response_object, 201
        else:
            
            response_object = {
                "status":"fail",
                "message": "Project not found"
            }
            return response_object, 404
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})

def get_projects_by_empId(status, empId):
    try:
        project = mongo.db.jobs.find({"status":status, "employerId": empId})
        if project is not None:
            response_object = {
                "status":"success",
                "data": list(project)
            }
            return response_object, 201
        else:
            
            response_object = {
                "status":"fail",
                "message": "No projects found"
            }
            return response_object, 404
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})
    
def get_all_projects():
    try:
        job = mongo.db.jobs.find({})
        print(job.count())
        #return jsonify({"data": candidates.count()})
        response_object = {
            "status":"success",
            "data": list(job)
        }
        print(list(job))
        return response_object, 200
        #return jsonify({"data": list(job), "job_count":job.count()})
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})


def update_a_project(data):
    try:
        project = mongo.db.jobs.find_one({"projectId":data["projectId"]})
        if project is not None:
            mongo.db.jobs.update_one({"projectId":data["projectId"]}, {"$set":data}, upsert=True) 
            response_object = {
                "status": "success",
                "data": "Project successfully updated"
            }      
            return  response_object, 201                            
        else:
            response_object = {
                "status": "success",
                "data": "Project does not exist"
            }      
            return  response_object, 404  

    except Exception as e:
        response_object = {
                "status": "success",
                "meaasge": "Something went, try again"
            }      
    return  response_object, 500 
    

def get_a_project_by_titleId():
    pass

def get_a_project_by_empId():
    pass

def delete_a_project(projectId):
    try:
        project = mongo.db.jobs.find_one({"projectId": projectId})
        if project is not None:
            
            mongo.db.jobs.update_one({"projectId": projectId}, {"$set":{"active":False}})
            response_object = {
                "status":"success",
                "message": "Project was successfully deleted"
            }
            return response_object, 201
        else:
            
            response_object = {
                "status":"fail",
                "message": "Project not found"
            }
            return response_object, 404
    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})



def new_proposal(data):
    try:
        
        room_members = data['room_members']
        new_data =  {
            'developerId': data['developerId'],
            'employerId': data['employerId'],
            'projectId' : data['projectId'],
            'project_title'  : data['project_title'],
            'titleId' : data['titleId'],
            'firstname'  : data['firstname'],
            'lastname'  : data['lastname'],
            'email' : data['email'],
            'bid'  : data['bid'],
            'estimated_finish_time' : data['estimated_finish_time'],
            'cover_letter'  : data['cover_letter'],
            'created_on'  : data['created_on'],
            'avatar':data['avatar']
        }

        prop = mongo.db.proposal.find_one({"developerId": new_data['developerId'], "projectId":new_data['projectId'] }, {"_id": 0})
        if prop is not None:
            response_object = {
                "status":"fail",
                "message": "Already sent a proposal for this project"
            }
            return response_object, 201
            
        else:
    
            new_data['_id'] = str(ObjectId())
            proposal_id = mongo.db.proposal.insert_one(new_data).inserted_id
    
            if proposal_id is not None:
                #Update project initial_route to proposals
                x = mongo.db.jobs.update_one({'_id':new_data['projectId']}, {"$set": {'initial_route':'proposals'}})
                
            # Create new chat room
            
            add_room(proposal_id, new_data['employerId'], new_data['developerId'], new_data['created_on'], room_members, new_data['firstname'], new_data['lastname'], new_data['avatar'], new_data['project_title'])

            # Update project bid 
            update_project(data['projectId'], data['bid'])
            
            response_object = {
                "status":"success",
                "message": "proposal successfully sent"
            }
            return response_object, 201

    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})


def update_a_proposal(data):
    try:
        proposal = mongo.db.proposal.find_one({"_id":data["proposalId"]})
        print(data["proposalId"])
        if proposal is not None:
            mongo.db.proposal.update_one({"_id":data["proposalId"]}, {"$set":data}, upsert=True) 
            response_object = {
                "status": "success",
                "meaasge": data
            }      
            return  response_object, 201                            
        else:
            response_object = {
                "status": "fail",
                "meaasge": "Proposal does not exist"
            }      
            return  response_object, 404  

    except Exception as e:
        response_object = {
                "status": "success",
                "meaasge": "Something went, try again"
            }      
    return  response_object, 500  


def get_a_proposal_by_projectId(projectId):
    
    try:
        results = mongo.db.proposal.aggregate([
            {
            "$match": { 'projectId': projectId}
            },
            {
                "$lookup": {
                "from": 'users',
                "foreignField": 'public_id',
                "localField": 'developerId',
                "as": 'user'
                }
            },
            {
                "$unwind":"$user"
            }
        ])
        
        response_object = {
            "status": "success",
            "message": list(results)
        }
        print(list(results))
        
        return response_object, 201
       
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": e
        }
        return response_object, 500

def get_a_proposal_by_titleId(titleId):
    
    try:
        results = mongo.db.proposal.aggregate([
            {
            "$match": { 'titleId': titleId}
            },
            {
                "$lookup": {
                "from": 'users',
                "foreignField": 'public_id',
                "localField": 'developerId',
                "as": 'user'
                }
            },
            {
                "$unwind":"$user"
            }
        ])
        
        response_object = {
            "status": "success",
            "message": list(results)
        }
        print(list(results))
        
        return response_object, 201
       
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": e
        }
        return response_object, 500



def get_a_proposal(proposalId):
    try:
        proposal = mongo.db.proposal.find_one({'_id':proposalId})

        response_object = {
            "status": "success",
            "message": proposal
        }
        return response_object, 201
        
    except Exception as e:
        
        response_object = {
            "status": "fail",
            "message": "Something went wrong. Try again"
        }
        return response_object, 500


def delete_a_proposal(proposalId):
    try:
        proposal = mongo.db.proposal.find_one({'_id':proposalId})
        if proposal is not None:
            mongo.db.proposal.update_one({'_id':proposalId}, {"$set":{"active":False}})
            response_object = {
                "status": "success",
                "message": "Proposal was deleted successfully"
            }
            return response_object, 201
        else:
            response_object = {
                "status": "success",
                "message": "Proposal does not exist"
            }
            return response_object, 404

    except Exception as e:
        
        response_object = {
            "status": "fail",
            "message": "Something went wrong. Try again"
        }
        return response_object, 500

def get_all_proposals():
    try:
        proposal = mongo.db.proposal.find({})

        response_object = {
            "status": "success",
            "data": proposal
        }
        return response_object, 201
        
    except Exception as e:
        
        response_object = {
            "status": "fail",
            "message": "Something went wrong. Try again"
        }
        return response_object, 500



#######################
# HIRE & OFFERS       #
#######################

def make_offer(data):
    try:
     
        milestone_data = {
             'developerId' : data['developerId'],
             'employerId': data['employerId'],
             'projectId': data['projectId'],
             'project_title' : data['title'],
             'milestone_task' : data['milestone_task'],
             'milestone_amount' : data['milestone_amount'],
             'milestone_due_date' : data['milestone_due_date'],
             'status' : 'In progress',
             'created_on' : data['created_on']
        }

        contract_data = {
            "developerId" : data["developerId"],
            "payeeToken" : data["payeeToken"],
            "projectId" : data["projectId"],
            "developer_firstname" : data["developer_firstname"],
            "developer_lastname" : data["developer_lastname"],
            "developer_email" : data["developer_email"],
            "employerId" : data["employerId"],
            "employer_firstname" : data["employer_firstname"],
            "employer_lastname" : data["employer_lastname"],
            "employer_email" : data["employer_email"],
            "company_name" : data["company_name"],
            "title" : data["title"],
            "job_description": data["job_description"],
            "payment_type": data["payment_type"],
            "total_project_cost": data["total_project_cost"],
            "created_on": data["created_on"]
        }

        
        # Create contract collection
        contract_data["_id"] = str(ObjectId())
        contractId = mongo.db.contracts.insert_one(contract_data).inserted_id
        
        if contractId is not None:
            # Update project to inprogress / initial_route = inprogress
            mongo.db.jobs.update_one({"_id":data["projectId"]}, {"$set":{"status":"in-progress", "initial_route":"payments"}})
            
            # Create milestones collection
            milestone_data['_id'] = str(ObjectId())
            milestone_data['contractId'] = contractId
            mongo.db.milestones.insert_one(milestone_data)

            # Check if customer exist
            check_customer = mongo.db.customers.find_one({'employerId':request.form['employerId']})
            if check_customer is None:
                # Create new customer on Braintree
                cust_data = {
                    "first_name": data["employer_firstname"],
                    "last_name": data["employer_lastname"],
                    "company": data["company_name"],
                    "email": data["employer_email"],
                }
                # Create a new Braintree customer_id 
                result = create_customer(cust_data)
                print(result)
               
                # insert new customer details in transaction collection on devporte db
                data = {
                    "first_name": data["employer_firstname"],
                    "last_name": data["employer_lastname"],
                    "company": data["company_name"],
                    "email": data["employer_email"],
                    "employerId": data["employerId"]
                }
                
                data['_id'] = result.customer.id
                mongo.db.customers.insert_one(data)
                response_object = {
                    "success":"success",
                    "message": result.customer.id
                }
                return response_object, 201
            else:

                # Customer already exist get the customerId
                cust = mongo.db.customers.find_one({'employerId':request.form['employerId']})

                response_object = {
                    "status":"success",
                    "message":cust['_id']
                }

                return response_object, 201
                
        return jsonify({"data": "contractId"})
    except Exception as e:

        response_object = {
            "status":"fail",
            "message":e
        }
        return response_object, 500


def new_milestone():
    
    try:
        
        #convert form data to json
        contractId = request.form['contractId']
       
        milestone = {
             'developerId' : request.form['developerId'],
             'employerId' : request.form['employerId'],
             'projectId' : request.form['projectId'], 
             'project_title': request.form['title'],
             'milestone_task' : request.form['milestone_task'],
             'milestone_amount' : int(request.form['milestone_amount']),
             'milestone_due_date' : request.form['milestone_due_date'],
             'status' : request.form['status'],
             "created_on" : request.form['created_on'],
             'contractId' : request.form['contractId']
        }
        
        
        check = mongo.db.contracts.find_one({'_id':request.form['contractId']})
        if check is not None:
            print(contractId)
           
            # Create milestone
            milestone['_id'] = str(ObjectId())
            mongo.db.milestones.insert_one(milestone)

            # Customer already exist get the customerId
            cust = mongo.db.customers.find_one({'employerId':request.form['employerId']})
            
            return jsonify({"data":cust['_id']})
            
        else:

            # return none

            return jsonify({"data": "No hires for this project yet"})
                


       #return jsonify({"msg": "Milestone successfully created"})

    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})



