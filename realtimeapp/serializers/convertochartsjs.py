from . import THERMOHYGRO 
import numpy as np 

def readings_to_matrix(raw_readings):
    '''
    Get all readings and transform them into a list of touples.
    Each touple is a reading comprising reading Id, date, temperature 
    and humidity.
    '''
    readings_list = dict.items(raw_readings)
    readings_matrix=[]

    for readings_touples in readings_list:

        readingid=readings_touples[0]
        date=readings_touples[1]['date']
        temperature=readings_touples[1]['temperature']
        humidity=readings_touples[1]['humidity']

        readings_matrix.append([readingid, date, temperature, humidity])
    
    return readings_matrix

def get_statistics(readings_matrix):
    '''
    Find statistics for a given set of readings.
    '''
    matrix_filtered = np.delete(readings_matrix,0,axis=1)
    matrix_filtered = np.delete(matrix_filtered,0,axis=1)
    # First and second collums are reading ID and date

    float_matrix = np.ndarray.astype(matrix_filtered,float)
    # data comes as strings from REST api

    mean = np.mean(float_matrix,axis=0)
    std = np.std(float_matrix,axis=0)
    minimum = np.min(float_matrix,axis=0)
    maximum = np.max(float_matrix,axis=0)
    argmin = np.argmin(float_matrix,axis=0)
    argmax = np.argmax(float_matrix,axis=0)
    median = np.median(float_matrix,axis=0)
    percentile = np.percentile(float_matrix,axis=0,q=98)
    return mean, std, minimum, maximum, argmin, argmax, median, percentile

def generate_stats_from_raw(raw_readings):
    
    readings_matrix = readings_to_matrix(raw_readings)
    stats = get_statistics(readings_matrix)
    json_stats = {
                'tempmean': stats[0][0], 
                'tempmedian': stats[6][0], 
                'tempmin': stats[2][0], 
                'tempmindate': readings_matrix[stats[4][0]][1], 
                'tempmax': stats[3][0], 
                'tempmaxdate': readings_matrix[stats[5][0]][1], 
                'hummean': stats[0][1], 
                'hummedian': stats[6][1], 
                'hummin': stats[2][1],
                'hummindate': readings_matrix[stats[4][1]][1],
                'hummax': stats[3][1], 'hummaxdate': readings_matrix[stats[5][1]][1]
                }
    
    return json_stats

     