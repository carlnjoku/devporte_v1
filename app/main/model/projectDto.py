from flask_restplus import Namespace, fields
from werkzeug.datastructures import FileStorage


class ProjectDto:
    api = Namespace('project', description='Project related operations')

    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files',
                            type=FileStorage, required=True)

    project = api.model('project_details', {
        'public_id': fields.String(required=True, description='user public_id'),
        'employerId': fields.String(required=True, description='user password'),
        'company_name': fields.String(required=True, description='user password'),
        'firstname': fields.String(required=True, description='user password'),
        'lastname': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user password'),
        'title': fields.String(required=True, description='user password'),
        'titleId': fields.String(required=True, description='user password'),
        'job_description': fields.String(required=True, description='user password'),
        'project_type': fields.String(required=True, description='user password'),
        'required_skills': fields.List(fields.Raw,required=True, description='user password'),
        'experience_level': fields.String(required=True, description='user password'),
        'payment_type': fields.String(required=True, description='user password'),
        'project_timeline': fields.String(required=True, description='user project_time'),
        'budget': fields.String(required=True, description='user password'),
        'bid': fields.List(fields.Integer, required=True, description='user password'),
        'created_on': fields.String(required=True, description='user password'),
        'initial_route': fields.String(required=True, description='user password'),
        'status': fields.String(required=True, description='user password')
    })

    project_update = api.model('project_details', {
        'projectId': fields.String(required=True, description='projectId'),
        'public_id': fields.String(required=True, description='employer public_id'),
        'employerId': fields.String(required=True, description='employer employerId'),
        'company_name': fields.String(required=True, description='user password'),
        'firstname': fields.String(required=True, description='user password'),
        'lastname': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user password'),
        'title': fields.String(required=True, description='user password'),
        'titleId': fields.String(required=True, description='user password'),
        'job_description': fields.String(required=True, description='user password'),
        'project_type': fields.String(required=True, description='user password'),
        'required_skills': fields.List(fields.Raw,required=True, description='user password'),
        'experience_level': fields.String(required=True, description='user password'),
        'payment_type': fields.String(required=True, description='user password'),
        'project_timeline': fields.String(required=True, description='user project_time'),
        'budget': fields.String(required=True, description='user password'),
        'bid': fields.List(fields.Integer, required=True, description='user password'),
        'created_on': fields.String(required=True, description='user password'),
        'initial_route': fields.String(required=True, description='user password'),
        'status': fields.String(required=True, description='user password')
    })

    proposal = api.model('proposal', {
        "developerId" :fields.String(required=True, description=''),
        "employerId" :fields.String(required=True, description=''),
        "projectId":fields.String(required=True, description=''),
        "titleId" :fields.String(required=True, description=''),
        "project_title"  :fields.String(required=True, description=''),
        "firstname"  :fields.String(required=True, description=''),
        "lastname"  :fields.String(required=True, description=''),
        "email" :fields.String(required=True, description=''),
        "bid"  :fields.Integer(required=True, description=''),
        "estimated_finish_time" :fields.String(required=True, description=''),
        "cover_letter"  :fields.String(required=True, description=''),
        "created_on"  :fields.String(required=True, description=''),
        "avatar" :fields.Url(required=True, description=''), 
        'room_members': fields.List(fields.Raw,required=True, description='user password'),
       
    })

    update_proposal = api.model('update proposal', {
        "proposalId" :fields.String(required=True, description=''),
        "developerId" :fields.String(required=True, description=''),
        "employerId" :fields.String(required=True, description=''),
        "projectId":fields.String(required=True, description=''),
        "titleId" :fields.String(required=True, description=''),
        "project_title"  :fields.String(required=True, description=''),
        "firstname"  :fields.String(required=True, description=''),
        "lastname"  :fields.String(required=True, description=''),
        "email" :fields.String(required=True, description=''),
        "bid"  :fields.Integer(required=True, description=''),
        "estimated_finish_time" :fields.String(required=True, description=''),
        "cover_letter"  :fields.String(required=True, description=''),
        "created_on"  :fields.String(required=True, description=''),
        "avatar" :fields.Url(required=True, description='')
    })

    hire = api.model(' hire_offer', {
        "developerId" : fields.String(required=True, description=''),
        "projectId" : fields.String(required=True, description=''),
        "developerId" : fields.String(required=True, description=''),
        "payeeToken" : fields.String(required=True, description=''),
        "developer_firstname" : fields.String(required=True, description=''),
        "developer_lastname" : fields.String(required=True, description=''),
        "developer_email" : fields.String(required=True, description=''),
        "employerId" : fields.String(required=True, description=''),
        "employer_firstname" : fields.String(required=True, description=''),
        "employer_lastname" : fields.String(required=True, description=''),
        "employer_email" : fields.String(required=True, description=''),
        "company_name" : fields.String(required=True, description=''),
        "title" : fields.String(required=True, description=''),
        "job_description": fields.String(required=True, description=''),
        "payment_type": fields.String(required=True, description=''),
        "total_project_cost": fields.String(required=True, description=''),
        "milestone_task": fields.String(required=True, description=''),
        "milestone_amount": fields.Integer(required=True, description=''),
        "milestone_due_date" : fields.String(required=True, description=''),
        "created_on" : fields.String(required=True, description=''),
    })

    milestone = api.model('milestone', {
        'developerId' : fields.String(required=True, description=''),
        'employerId' : fields.String(required=True, description=''),
        'projectId' : fields.String(required=True, description=''), 
        'project_title': fields.String(required=True, description=''),
        'milestone_task' : fields.String(required=True, description=''),
        'milestone_amount' : fields.Integer(required=True, description=''),
        'milestone_due_date' : fields.String(required=True, description=''),
        'status' : fields.String(required=True, description=''),
        "created_on" : fields.String(required=True, description=''),
        'contractId' : fields.String(required=True, description='')
    })

"""
Create offer
{
  "developerId": "17f626d9-ece4-46f9-a33e-793573efcb92",
  "projectId": "5eaf1c43029c003b829d7768",
  "payeeToken": "usr-bf64a7be-bd52-40b6-a8ef-f37e83df70d9",
  "developer_firstname": "Tayo",
  "developer_lastname": "Oke",
  "developer_email": "tayo@yahoo.com",
  "employerId": "20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
  "employer_firstname": "Goerge",
  "employer_lastname": "Osakwe",
  "employer_email": "sonny16@flavoursoft.com",
  "company_name": "Cvdump",
  "title": "Selenium web scrapping",
  "job_description": "We need someone who can scrap the web for information",
  "payment_type": "fixed",
  "total_project_cost": "3000",
  "milestone_task": "Develop the landing page",
  "milestone_amount": 100,
  "milestone_due_date": "string",
  "created_on": "string"
}


proposal

{
    "developerId" : "17f626d9-ece4-46f9-a33e-793573efcb92",
    "employerId" : "20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
    "projectId" : "934dd8e4-1b26-49fc-92ee-a70c7b1a88b8",
    "project_title" : "Selenium web scrapping",
    "titleId" : "selenium-web-scrapping",
    "firstname" : "Tayo",
    "lastname" : "Oke",
    "email" : "tayo@yahoo.com",
    "bid" : 600,
    "estimated_finish_time" : "20",
    "cover_letter" : "Thanks for the opportunity to bid for this project. Hire me and i will deliver in a record time. I am ready to start now",
    "created_on" : "1588022324743",
    "avatar" : "https://firebasestorage.googleapis.com/v0/b/devporte-64919.appspot.com/o/media%2F5e47e537c1f8d023941a76c5-chinedu.jpeg?alt=media",
    "room_members": [
        {
            "userId":"17f626d9-ece4-46f9-a33e-793573efcb92",
            "created_on": "3892821111",
            "isRoomAdmin": true,
            "firstname":"Tayo",
            "lastname":"Oke"       },
        {
            "userId":"20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
            "created_on"  : "3892821111",
            "isRoomAdmin": false,
            "employer_firstname":"Goerge",
            "employer_lastname":"Osakwe"       }
    ]
}


Update proposal

{
    "proposalId" : "5eaf1faed10f7bcc78be7549",
    "developerId" : "17f626d9-ece4-46f9-a33e-793573efcb92",
    "employerId" : "20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
    "projectId" : "1a47cb7c-f00c-46e3-abdc-3a705f43130c",
    "project_title" : "Selenium web scrapping",
    "titleId" : "selenium-web-scrapping",
    "firstname" : "Tayo",
    "lastname" : "Oke",
    "email" : "tayo@yahoo.com",
    "bid" : 700,
    "estimated_finish_time" : "10",
    "cover_letter" : "I will bid for this project. Hire me and i will deliver in a record time. I am ready to start now",
    "created_on" : "1588022324743",
    "avatar" : "https://firebasestorage.googleapis.com/v0/b/devporte-64919.appspot.com/o/media%2F5e47e537c1f8d023941a76c5-chinedu.jpeg?alt=media"

}
"""


"""
{
  "public_id": "20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
  "employerId": "5eadf53ad70ffbac08608004",
  "company_name":"Cvdump",
  "firstname": "Goerge",
  "lastname": "Osakwe",
  "email": "sonny@flavoursoft.com",
  "title": "Selenium web scrapping",
  "titleId": "selenium-web-scrapping",
  "job_description": "We need someone who can scrap the web for information",
  "project_type": "hourly",
  "project_timeline": "3-6", 
  "required_skills": [ 
        {
            "tool_name" : "Python"
        }, 
        {
            "tool_name" : "Scala"
        }
    ],
  "experience_level": "expert",
  "payment_type": "fixed",
  "budget": "1000 plus",
  "bid": [800,200],
  "created_on": "string",
  "initial_route": "proposals",
  "status": "in-progress"
}
"""


"""
{
  "public_id": "20361ed8-1a0e-4caf-98a5-5b1c2b9ff4e5",
  "projectId":"cfb2811e-ff4b-4164-8d07-cf94cb40d747",
  "employerId": "5eadf53ad70ffbac08608004",
  "company_name":"Cvdump",
  "firstname": "Goerge",
  "lastname": "Osakwe",
  "email": "sonny@flavoursoft.com",
  "title": "Selenium web scrapping",
  "titleId": "selenium-web-scrapping",
  "job_description": "We need someone who can scrap the web for information",
  "project_type": "hourly",
  "project_timeline": "3-6", 
  "required_skills": [ 
        {
            "tool_name" : "Python"
        }, 
        {
            "tool_name" : "Scala"
        }
    ],
  "experience_level": "beginner",
  "payment_type": "fixed",
  "budget": "1000 plus",
  "bid": [800,200],
  "created_on": "string",
  "initial_route": "proposals",
  "status": "in-progress"
}
"""

    
