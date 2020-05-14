from flask import request
from flask_restplus import Resource

from ..model.projectDto import ProjectDto
from app.main.service.project_service import (new_project, get_all_projects, 
                                                get_a_project_by_empId, get_a_project_titleId, 
                                                get_a_project_projectId, update_a_project, 
                                                delete_a_project, get_projects_by_empId, new_proposal,
                                                update_a_proposal, get_a_proposal_by_projectId,
                                                get_a_proposal_by_titleId, get_a_proposal, delete_a_proposal,
                                                get_all_proposals, make_offer, new_milestone)

from app.main.service.sendemail_service import send_email_confirmation

api = ProjectDto.api
_project = ProjectDto.project
_project_update = ProjectDto.project_update
_proposal = ProjectDto.proposal
_update_proposal = ProjectDto.update_proposal
_hire = ProjectDto.hire
_milestone = ProjectDto.milestone

upload_parser = ProjectDto.upload_parser

@api.route('/')
class ProjectList(Resource):
    @api.doc('list_of_posted_projects')
    #@api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all posted projects"""
        return get_all_projects()
   
    @api.response(201, 'Project successfully created !')
    @api.doc('post a new project')
    #@api.expect(_project, validate=True)
    @api.expect(upload_parser, validate=True)
    def post(self):
        """Post a new Project """
        #data = request.json
        args = upload_parser.parse_args() # upload a file
        uploaded_file = args['file']
        req_data = request.form.to_dict(flat=True)
        return new_project(req_data, uploaded_file)

    @api.response(201, 'Project successfully updated !')
    @api.doc('update project')
    @api.expect(_project_update, validate=True)
    def put(self):
        """Update a Project """
        data = request.json
        return update_a_project(data=data)


@api.route('/<projectId>')
@api.param('projectId', 'The project identifier')
@api.response(404, 'Project not found.')

class Project(Resource):
    @api.doc('get a project')
    def get(self, projectId):
        """get a project with its identifier"""
        return get_a_project_projectId(projectId)
        
    @api.doc('delete a project')
    def delete(self, projectId):
        """delete a project with its identifier"""
        return delete_a_project(projectId)
    

@api.route('/tle/<titleId>')
@api.param('titleId', 'The project titleId')
@api.response(404, 'Project not found.')
class ProjectTitle(Resource):
    @api.doc('get a project by titleId')
    def get(self, titleId):
        """get a project with its titleId"""
        return get_a_project_titleId(titleId)

@api.route('/status/<status>/empid/<employerId>')
@api.param('empId', 'The project by employer identifier')
@api.response(404, 'Project not found.')
class ProjectEmp(Resource):
    @api.doc('Get a list of projects by status and employer Id')
    def get(self, status, employerId):
        """get a project with its status and employer Id"""
        return get_projects_by_empId(status, employerId)
        
##################################
# PROPOSAL
# ################################
#    
@api.route('/proposal')
class Proposal(Resource):
    @api.doc('list_of_proposals')
    @api.marshal_list_with(_proposal, envelope='data')
    def get(self):
        """List all sent proposals"""
        return get_all_proposals()
   
    
    @api.response(201, 'Proposal successfully sent !')
    @api.doc('send a new proposal')
    @api.expect(_proposal, validate=True)
    def post(self):
        """Send a new proposal """
        data = request.json
        return new_proposal(data=data)

    @api.response(201, 'Proposal successfully updated !')
    @api.doc('update proposal')
    @api.expect(_update_proposal, validate=True)
    def put(self):
        """Update a proposal """
        data = request.json
        return update_a_proposal(data=data)

@api.route('/proposal/<proposalId>')
@api.param('proposalId', 'The project by proposalId')
@api.response(404, 'Project not found.')
class Project(Resource):
    @api.doc('get a proposal by proposalId')
    def get(self, proposalId):
        """get a proposal with its proposalId"""
        return get_a_proposal(proposalId)
      

    @api.doc('get a proposal by proposalId')
    def delete(self, proposalId):
        """Delete a proposal with its proposalId"""
        project = delete_a_proposal(proposalId)
        if not project:
            api.abort(404)
        else:
            return project  

@api.route('/proposal/pid/<projectId>')
@api.param('projectId', 'The proposal by projectId')
@api.response(404, 'Proposal not found.')
class Project(Resource):
    @api.doc('get a proposal by projectId')
    def get(self, projectId):
        """get a proposal with its projectId"""
        return get_a_proposal_by_projectId(projectId)


@api.route('/proposal/tid/<titleId>')
@api.param('projectId', 'The proposal by titleId')
@api.response(404, 'Proposal not found.')
class Project(Resource):
    @api.doc('get a proposal by titleId')
    def get(self, titleId):
        """get a proposal with its project titleId"""
        return get_a_proposal_by_titleId(titleId)
        
################
# HiRE & OFFER #
################


@api.route('/hire')
class OfferList(Resource):
    @api.doc('list_of_hires')
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all hires"""
        return get_all_projects()

    @api.response(201, 'Offer was successfully sent to freelancer !')
    @api.response(401, 'Failed try again !')
    @api.doc('Make a new offer')
    @api.expect(_hire, validate=True)
    def post(self):
        """Make a new offer """
        data = request.json
        return make_offer(data=data)
    
    @api.response(201, 'Offer successfully updated !')
    @api.doc('update offer')
    @api.expect(_project, validate=True)
    def put(self):
        """Update an offer """
        data = request.json
        return update_a_project(data=data)

@api.route('/hire/<offerId>')
@api.param('offerId', 'The offer by offerId')
@api.response(404, 'Offer not found.')
class Offer(Resource):
    @api.doc('get an offer by offerId')
    def get(self, projectId):
        """get an offer with its offerId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 

    @api.doc('accept an offer by offerId')
    def get(self, projectId):
        """accept an offer with its offerId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 

    @api.doc('cancel an offer by offerId')
    def delete(self, projectId):
        """cancel an offer with its offerId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 


###################
# MILESTONES      #
###################

@api.route('/milestone')
class MilestoneList(Resource):
    @api.doc('list_of_milestones')
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all milestones"""
        return get_all_projects()

    @api.response(201, 'Milestone was successfully created !')
    @api.doc('Ceate a new milestone')
    @api.expect(_milestone, validate=True)
    def post(self):
        """Ceate a new milestone """
        data = request.json
        return new_milestone(data=data)
    
    @api.response(201, 'Milestone successfully updated !')
    @api.doc('update milestone')
    @api.expect(_project, validate=True)
    def put(self):
        """Update a milestone """
        data = request.json
        return update_a_project(data=data)

@api.route('/milestone/<milestoneId>')
@api.param('milestoneId', 'The milestone by milestoneId')
@api.response(404, 'Milestone not found.')
class Milestone(Resource):
    @api.doc('get a milestone by milestoneId')
    def get(self, projectId):
        """get a milestone with its milestoneId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 


    @api.doc('delete a milestone by milestoneId')
    def delete(self, projectId):
        """cancel an offer with its milestoneId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 



@api.route('/project_files')
@api.response(201, 'Proposal successfully sent !')
@api.doc('uploaded a new file')
@api.expect(_project, validate=True)
class ProjectFileUpload(Resource):
    def post(self):
        """Upload a new proposal """
        data = request.json
        return new_project(data=data)


@api.route('/project_files/<projectId>')
@api.param('projectId', 'The project by projectId')
@api.response(404, 'Project not found.')
class ProjectFiles(Resource):
    @api.doc('get a project files by projectId')
    def get(self, projectId):
        """get a project files with its projectId"""
        proj_files = get_a_project_by_titleId(projectId)
        if not proj_files:
            api.abort(404)
        else:
            return proj_files 
    

    @api.doc('delete a project files by projectId')
    def delete(self, projectId):
        """delete a project files with its projectId"""
        proj_files = get_a_project_by_titleId(projectId)
        if not proj_files:
            api.abort(404)
        else:
            return proj_files 

@api.route('/task')
class TaskList(Resource):
    @api.doc('list_of_proposals')
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all sent proposals"""
        return get_all_projects()

    @api.response(201, 'Task successfully sent !')
    @api.doc('create a new task')
    @api.expect(_project, validate=True)
    def post(self):
        """Create a new task """
        data = request.json
        return new_project(data=data)

    @api.response(201, 'Task successfully updated !')
    @api.doc('update task')
    @api.expect(_project, validate=True)
    def put(self):
        """Update a task """
        data = request.json
        return update_a_project(data=data)

@api.route('/task/<projectId>')
@api.param('projectId', 'The project by projectId')
@api.response(404, 'Project not found.')
class Task(Resource):
    @api.doc('get a project task by projectId')
    def get(self, projectId):
        """get a project task with its projectId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 

    @api.doc('delete a project task by projectId')
    def delete(self, projectId):
        """delete a project task with its projectId"""
        proj_task = get_a_project_by_titleId(projectId)
        if not proj_task:
            api.abort(404)
        else:
            return proj_task 



