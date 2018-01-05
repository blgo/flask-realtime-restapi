from flask_restful import Api


api = Api()


def create_api(app):

    from .resources import Reading, ReadingList


    api.add_resource(ReadingList, '/sensor1')
    api.add_resource(Reading, '/sensor1/<reading_id>')


    api.init_app(app)