from flask_restful import Api


api = Api()


def create_api(app):

    from .resources import TodoSimple
    
    # Configure resources
    api.add_resource(TodoSimple, '/<string:todo_id>')

    api.init_app(app)