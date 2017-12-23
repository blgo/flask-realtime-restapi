from flask import request
from flask_restful import Resource, reqparse#, inputs

parser = reqparse.RequestParser()
# parser.add_argument('data',type=inputs.regex('^\D+$') , help="data has to be a string")
parser.add_argument('data',type=int , help="data has to be a number")

todos = {}

#Add data to the server using: curl http://localhost:5000/todo1 -d "data=it works!" -X PUT

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id:todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id:todos[todo_id]}