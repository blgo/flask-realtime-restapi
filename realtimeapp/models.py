import datetime
from mongoengine import *
# TODO: Use https://flask-restful.readthedocs.io/en/latest/quickstart.html#data-formatting
# Sensor dictionary for temperature/humidity reading
# THERMOHYGRO = {
#     <string:RoomNameYYYYMMDDHHmmss> : { 'date': <datetime.isoformat>,
#                                         'room': <string: room name>,
#                                         'temperature': <int:Celcius>,
#                                         'humidity': <int> },
#     (...)
# }

# Establishing a Connection
connect('mongoengine_test', host='localhost', port=27017)


# Defining a Document
class Post(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)
    author = StringField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)

# Saving Documents
post_1 = Post(
    title='Sample Post',
    content='Some engaging content',
    author='Scott'
)
post_1.save()       # This will perform an insert
print(post_1.title)
post_1.title = 'A Better Post Title'
post_1.save()         # This will perform an atomic edit on "title"
print(post_1.title)

post_2 = Post(content='Content goes here', author='Michael')
post_2.save()
