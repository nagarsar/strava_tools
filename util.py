from datetime import datetime,timedelta
from math import sin, cos, sqrt, atan2, radians, degrees
import time as timelibrary


def get_distance(coordinates=[52.2296756, 21.0122287, 52.406374, 16.9251681]):
    """
    input cordinates of 2 points A and B e.g [Alat, Alon, Blat, Blon]
    return distance [m] 
    """
    R = 6373.0 # approximate radius of earth in km

    lat1 = radians(float(coordinates[0]))
    lon1 = radians(float(coordinates[1]))
    lat2 = radians(float(coordinates[2]))
    lon2 = radians(float(coordinates[3]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    unit = "degree"
    if unit == "degree":
        dlon = degrees(dlon)
        dlat = degrees(dlat)

    return distance, dlon, dlat


def get_time_delta(date1, date2, plage=5000):
    """
    inputs date format : yyyy-mm-dd
    return tuple
    abs val of days between date1 and date2
    the percentage difference between date1 and date2 considering a range
    """
    delta_days=0
    percentage=1.0
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")

        delta = d2 - d1
        delta_days = abs(delta.days)
        plage = plage 
        percentage = (-delta_days + plage)/plage
    except:
        pass

    return delta_days, percentage


def get_time_delta_seconds(date1, date2):
    """
    inputs date format : yyyy-mm-dd
    return delta dates [s]
    """
    delta_seconds=0
    try:
        delta = date2 - date1
        delta_seconds = abs(delta.seconds)
    except:
        pass

    return delta_seconds


def get_date_after_x_days(date1, days):
    """
    inputs date format : yyyy-mm-dd and number of days
    return 
    date with format yyyy-mm-dd
    """
    date_1 = datetime.strptime(date1, "%Y-%m-%d")

    end_date = date_1 + timedelta(days=days)
    end_date = end_date.strftime("%Y-%m-%d")

    return end_date


def convert_time(value):
    """
    input str value e.g '1:15' or 75s
    return result [s] e.g 75
    """
    if ':' in value:
        minuts = value.split(':')[0]
        second = value.split(':')[1]
        result = int(minuts * 60 + second)

    if 's' in value:
        second = value.split('s')[0]
        result = int(second)

    return result


def get_timestamp(time, pattern):
    """
    input time str e.g. 2021-08-20T06:48:14Z with, pattern e.g."%Y-%m-%dT%H:%M:%SZ"
    return timestamp
    """
    timestamp = timelibrary.mktime(timelibrary.strptime(time, pattern))
    
    return timestamp


def get_datetime(timestamp):
    """
    input timestamp
    return a datetime object
    """
    calculated_time = datetime.fromtimestamp( float(timestamp) )

    return calculated_time

def get_str_time(datetimeobj, pattern="%Y-%m-%dT%H:%M:%SZ"):
    """
    input a datetimeobj, time pattern
    return str time
    """
    str_time = datetimeobj.strftime(pattern)

    return str_time

def convert_speed(time:int, distance:float, unit="km_h"):
    """
    input delta time [s], distance [m], str desired speed units (m_s/km_h)
    return speed
    """
    if unit=="km_h":
        result = (distance/1000) / (time/3600)

    if unit=="m_s":
        result = distance / time

    return result