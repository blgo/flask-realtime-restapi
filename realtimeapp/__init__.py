from flask import Flask
from .restful import api
from .resources_extended import ReadingListSocketioEvent

app = Flask(__name__)


def configure_app():
    app.config['SECRET_KEY'] = "verysecret"
    
    from . import routes

    return app

# Include and initialise resources
def create_api(app):

    from .restful.resources import Reading

    api.add_resource(Reading, '/sensor1/<reading_id>')
    api.add_resource(ReadingListSocketioEvent, '/sensor1')


    api.init_app(app)

