from .restful.resourcesreadings import ReadingList
from .socketio.charts_events import emit_new_reading


# Inheritance seems easier to implement, and allows me to test the RESTful
# module with and without socketIO
class ReadingListSocketioEvent(ReadingList):
    '''
    Add SocketIO call on top of RESTful api resources sensors   
    '''
    
    def get(self):
        return super().get()

    def post(self):
        result = super().post()
        
        emit_new_reading(result[0])        
        return result
