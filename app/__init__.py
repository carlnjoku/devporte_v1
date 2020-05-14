from flask_restplus import Api
from flask import Blueprint


from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.projects_controller import api as project_ns
from .main.controller.finances_controller import api as finance_ns
from .main.controller.socketio_controller import api as socket_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Devporte application APIs',
          version='1.0',
          description='A web service for web and mobile'
          )

api.add_namespace(user_ns, path='/api/v1/user')
api.add_namespace(auth_ns, path='/api/v1/auth')
api.add_namespace(project_ns, path='/api/v1/project')
api.add_namespace(finance_ns, path='/api/v1/finance')