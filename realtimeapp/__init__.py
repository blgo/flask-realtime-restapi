from flask import Flask
from .restful.resources import ReadingList
from .restful import api
from .socketio.charts_events import emit_new_reading

app = Flask(__name__)

# Inheritance seems easier to implement, and allows me to test the RESTful
# module with and without socketIO
class ReadingListSocketioEvent(ReadingList):
    '''
    Add SocketIO call on top of RESTful api resources   
    '''
    
    def get(self):
        return super().get()

    def post(self):
        result = super().post()
        emit_new_reading(result[0])        
        return result


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

