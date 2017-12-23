from flask_restful import Api


api = Api() # api.init_app(app) does not seem to work on create_api, check Blueprints for flask-restful


def create_api(app):

    from .resources import TodoSimple

    api = Api(app)
    
    # Configure resources
    api.add_resource(TodoSimple, '/<string:todo_id>')
    
    return app
