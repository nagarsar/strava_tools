from datetime import datetime
from numpy.lib import utils
import requests
import json
import os
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from secrets import refresh_token, access_token, key_secret ,client_id
from util import *
from rate import *


def refresh(write=False):

    access_token_file = "access_token"
    if os.path.exists(access_token_file):
        mts = datetime.fromtimestamp( os.stat(access_token_file).st_mtime )
        ts = datetime.now()

        delta_seconds = get_time_delta_seconds(mts, ts)
        if delta_seconds < 3600:
            access_token = open(access_token_file, 'r').read()
            print("Reuse Access Token = [{}]\n".format(access_token))
            return access_token


    payload = {
        'client_id': client_id,
        'client_secret': key_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    query = "https://www.strava.com/oauth/token"

    print("Requesting Token...\n")
    response = requests.post(query, 
        data=payload, 
        verify=False)

    access_token = response.json()['access_token']

    if write:
        with open(access_token_file, "w") as out:
            out.write(access_token)

    print("Access Token = {}\n".format(access_token))

    return access_token


def update_activity_description(activity_id, description):
    
    query = f"https://www.strava.com/api/v3/activities/{activity_id}"
    
    response = requests.put(query, 
        data={"description": description},
        headers={'Authorization': 'Bearer ' + access_token})
    set_quota(1)
    
    print(access_token, response)


def get_summary_poline():

    query = "https://www.strava.com/api/v3/athlete/activities"

    response = requests.get(query, 
        headers={'Authorization': 'Bearer ' + access_token}, 
        params={'per_page': 200, 'page': 1}
    ).json()
    set_quota(1)

    print(response[0]["name"])
    print(response[0]["map"]["summary_polyline"])


    return response[0]["map"]["summary_polyline"]


def get_activities():
    
    query = "https://www.strava.com/api/v3/athlete/activities"

    response = requests.get(query, 
        headers={'Authorization': 'Bearer ' + access_token}, 
        params={'per_page': 200, 'page': 1}
    ).json()
    set_quota(1)


    with open('json_objects/activities.json', 'w', encoding="utf-8", newline='\r\n') as output:
        json.dump(response, output, ensure_ascii=False, indent=4)

    return response


def get_activity(activity_id):
    
    query = f"https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts="


    response = requests.get(query, 
        headers={'Authorization': 'Bearer ' + access_token}, 
        params={'per_page': 200, 'page': 1}
    ).json()
    set_quota(1)

    with open('json_objects/activity.json', 'w', encoding="utf-8", newline='\r\n') as output:
        json.dump(response, output, ensure_ascii=False, indent=4)
    
    return response


def get_segments(coordinates=[]):
    
    query = "https://www.strava.com/api/v3/segments/explore?&activity_type=&min_cat=&max_cat="

    if not coordinates:
        print("Can't return segments. Please specify coordinates")
        return

    new_coordinates = [round(float(x),6) for x in coordinates]
    coordinates = list(map(str, new_coordinates))
    print(coordinates)
    response = requests.get(query, 
        headers={'Authorization': 'Bearer ' + access_token}, 
        params={
            'bounds' : ','.join(coordinates),
            'min_cat': '',
            'max_cat': '',
        }
    ).json()
    set_quota(1)

    with open('json_objects/segments.json', 'w', encoding="utf-8", newline='\r\n') as output:
        json.dump(response, output, ensure_ascii=False, indent=4)

    return response


def get_segment_by_id(id):
    
    query = "https://www.strava.com/api/v3/segments/{}".format(id)

    response = requests.get(query, 
        headers={'Authorization': 'Bearer ' + access_token}, 
        params={}
    ).json()
    set_quota(1)

    with open('json_objects/segment.json', 'w+', encoding="utf-8", newline='\r\n') as output:
        json.dump(response, output, ensure_ascii=False, indent=4)

    return response