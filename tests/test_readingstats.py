from realtimeapp.readingstats import *
from nose.tools import *

readings = {
    'bedroom20181815170112298831': 
    {'date': '2018-01-15 17:18:12.298831', 'room': 'bedroom', 'temperature': 20, 'humidity': 60},
    'bedroom20181815170113326091': 
    {'date': '2018-01-15 17:18:13.326091', 'room': 'bedroom', 'temperature': 11, 'humidity': 61}, 
    'bedroom20181815170114343102':
    {'date': '2018-01-15 17:18:14.343102', 'room': 'bedroom', 'temperature': 17, 'humidity': 57}
}

def test_readings_to_matrix():

    readings_matrix = readings_to_matrix(readings)
    assert_equal(readings_matrix[0][1],"2018-01-15 17:18:12.298831")
    assert_equal(readings_matrix[2][3], 57)


def test_get_statistics():
    readings_matrix = readings_to_matrix(readings)
    touple_stats = get_statistics_matrix(readings_matrix)
    assert_equal(touple_stats[0][1],59.333333333333336)
    assert_equal(touple_stats[6][1],60.0)


def test_generate_stats_from_raw():
    '''
    Gets the date for the minimum temperature
    '''
    stats = generate_stats(readings)
    assert_equal(stats['tempmindate'],'2018-01-15 17:18:13.326091')
