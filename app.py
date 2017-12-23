from flask import render_template
from flask_restful import Api
# from threading import Lock

from realtimeapp.resources.restfulapi import TodoSimple

from realtimeapp.socketio import create_app, socketio

app = create_app(debug=True)


# RESTful api
# Test endpoint:
# curl http://localhost:5000/todo1 -d "data=it works!" -X PUT
api = Api(app)
api.add_resource(TodoSimple, '/<string:todo_id>')

# thread = None
# thread_lock = Lock()

# # use websockets in background when new data is created
# global thread
# with thread_lock:
#     thread = socketio.start_background_task(target=background_thread)


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     socketio.emit('my_restful_data',
#                 {'data': data 'count': count},
#                 namespace='/test')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)