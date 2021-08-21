import time
import strava
from util import *


def scrap_commuting_speed_from_average():
    """
    From gps values, read from splits contained in 
    desired location the avg speed abd return it.
    WIP : 
    """

    activities = strava.get_activities()
    last_activity = activities[0]
    last_activity_id = last_activity['id']

    strava.update_activity_description(last_activity_id, "ereerer")

    activity = strava.get_activity(last_activity_id)
    coordinates = []
    for segment in activity['segment_efforts']:
        coordinates.append({
            'time':segment['start_date'],
            'coords': [
                segment['segment']['start_latitude'],
                segment['segment']['start_longitude']
            ]
        })

    # coordinates regent parc entrance (diagonal bot left - top right)
    coordiantes_regent = [51.52312775086868, -0.16276342541150055, 51.53754447798499, -0.1471422406193963] 
    
    print(coordinates)

    times_in_area = [] 
    for c in coordinates:

        if c['coords'][0] > coordiantes_regent[0] and \
            c['coords'][0] < coordiantes_regent[2]:
            
            if c['coords'][1] > coordiantes_regent[1] and \
                c['coords'][1] < coordiantes_regent[3]:

                times_in_area.append(c['time'])
                print(c['time'])

    start_area = times_in_area[0]
    end_area = times_in_area[-1]

    print("-----------")
    start_activity = activity['start_date']
    start_activity_ts = get_timestamp(start_activity, "%Y-%m-%dT%H:%M:%SZ")
    elapsed_time = activity['elapsed_time']
    end_activity = get_datetime(float(start_activity_ts) + float(elapsed_time)).strftime("%Y-%m-%dT%H:%M:%SZ")
    average_speed = activity['average_speed']
    print(end_activity)


def update_activity_description_with_laps():
    """
    Display in activity description the laps avg speed.
    """
    activities = strava.get_activities()
    time.sleep(1)
    last_activity = activities[0]
    last_activity_id = last_activity['id']

    visu1 = '\n--------------------------\n'
    activity = strava.get_activity(last_activity_id)
    description = str(activity['description'])
    if visu1 in description:
        return
    description = description + visu1 
    laps = activity['laps']
    for i,lap in enumerate(laps):
        description += 'lap' + str(i + 1) + str(': ') + str("{:.2f}".format(lap['average_speed'] * 3.6)) + ' km/h \n'

    print(f"editing activity description with :{description[:-1]}")
    strava.update_activity_description(last_activity_id, description[:-1])



if __name__ == '__main__':

    access_token = strava.refresh(write=True)

    update_activity_description_with_laps()