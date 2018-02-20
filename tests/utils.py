from mongoengine import connect
from realtimeapp.models import Sensor, ThermHygReading
from datetime import datetime

class TestDbUtils(object):
    def __init__(self):
        # Connect to the mock database
        
        connect(is_mock=True)
        
        # return_all_readings() output example
        # self.readings_sample = {
        #     'bedroom20181815170112298831': 
        #     {'date': '2018-01-15 17:18:12.298831', 'room': 'bedroom', 'temperature': 20, 'humidity': 60},
        #     'bedroom20181815170113326091': 
        #     {'date': '2018-01-15 17:18:13.326091', 'room': 'bedroom', 'temperature': 11, 'humidity': 61}, 
        #     'bedroom20181815170114343102':
        #     {'date': '2018-01-15 17:18:14.343102', 'room': 'bedroom', 'temperature': 17, 'humidity': 57}
        # }

        # Register a sensor
        self.sensor1_doc = Sensor.objects(name='Thermohydrometer')
        if not self.sensor1_doc:
            sensor1 = Sensor(room='backyard_test', name='Thermohydrometer')
            self.sensor1_doc = sensor1.save()


        # Save test readings
        self.reading_1 = ThermHygReading(
            sensor= self.sensor1_doc,
            temperature=15,
            humidity=99,
            date= datetime.now().isoformat(),
            readingid = 'backyard_test_1234567859abc'
        )
        self.reading_1_doc = self.reading_1.save()       # This will perform an insert

        self.reading_2 = ThermHygReading(
            sensor=self.sensor1_doc,
            temperature=11.1,
            humidity=51.5,
            date= datetime.now().isoformat(),
            readingid = 'backyard_test_1234567859abd'
        )
        self.reading_2_doc = self.reading_2.save()

        # Temperature should be float not string
        self.reading_3 = ThermHygReading(
            sensor= self.sensor1_doc,
            temperature='string',
            humidity=51.5,
            date='2018-01-05T16:50:21.114721',
            readingid = 'backyard_test_1234567859abe'
        )
        # reading_3 contains errors in order to test validation
        # The save command is trigger during the test to catch Exception

        self.reading_4 = ThermHygReading(
            sensor=self.sensor1_doc,
            temperature=12.2,
            humidity=52.2,
            date= '2018-01-05T16:50:21.114721',
            readingid = 'backyard_test_1234567859abf'
        )
        self.reading_4_doc = self.reading_4.save()
