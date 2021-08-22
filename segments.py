import strava
from util import *
import pandas as pd
import rate
import time




def generate_segments_report(output_file="strava_template.csv",coordinates=[], step=0):
    """
    inputs:
     - output filename
     - coordinates of the area to cover
     - step : distance in km for intermediates areas in the area to cover, 0 to disable
    outputs:
     - csv file : reports/ts_<output_file>
    return (None)
    """
    rows=[]
    if not coordinates:
        coordinates = [36.0, -94.1, 36.1, -94.0]
   
    all_coordinates=[]
    all_coordinates.append(coordinates)
    distance = get_distance(coordinates)     # km
    
    print(f"Given area: {distance[0]}km, | Step: {step}km")

    nb_zones_to_fetch = distance[0]/step
    nb_segments_per_zones = 10
    nb_token_needed = nb_zones_to_fetch * nb_segments_per_zones
    token_used = rate.get_data('quota_day')
    max_slot_15_per_day = 10
    secs_per_15 = 900
    if nb_token_needed <= 100:
        #instantaneous
        seconds_needed = 10
    if 100 < nb_token_needed and nb_token_needed <= 1000:
        # 1 day 
        slot_15_needed = nb_token_needed / 100
        seconds_needed = slot_15_needed * secs_per_15
    if 1000 < nb_token_needed:
        # more than 1 day
        slot_day_needed = nb_token_needed / 1000
        for i in range(1, slot_day_needed + 1):
            if i == slot_day_needed:
                token_used = token_used + (slot_day_needed * 1000)
                nb_token_needed = nb_token_needed - token_used
                slot_15_needed = nb_token_needed / 100
            slot_15_needed = max_slot_15_per_day
        seconds_needed = slot_day_needed * 172800 + slot_15_needed * secs_per_15
    time_it_takes = f"{int(seconds_needed/172800)}d {int(seconds_needed%172800/3600)}h {int(seconds_needed%172800%3600/60)}m {int(seconds_needed%172800%3600%60)}s"
    
    print(f"Assuming there is no parraleles jobs... \nIt will take {time_it_takes} to run this program.")
    
    if step:
        zones_nb  = int(distance[0] / step)      # number of zones
        zone_lat = float(distance[1] / zones_nb) # lat range zone
        zone_lon = float(distance[2] / zones_nb) # lon range zone
        
        print(f"Zones to fetch: {zones_nb}")

        lat1 = float(coordinates[0])
        lat2 = float(coordinates[0]) + zone_lat
        lon1 = float(coordinates[1])
        lon2 = float(coordinates[1]) + zone_lon
        all_coordinates.append([lat1,lon1,lat2,lon2])

        for i in range(0,zones_nb):
            lat1 = lat2
            lat2 = lat2 + zone_lat
            lon1 = lon2
            lon2 = lon2 + zone_lon
            all_coordinates.append([lat1,lon1,lat2,lon2])

    for coord in all_coordinates:

        segments = strava.get_segments(coord)
        if 'segments' not in segments:
            print(f"could fetch segments for {coord} segment obj content:{segments}")
            continue

        # 15 min test
        if not rate.get_data('quota_15') <= 90:
            # wait 15 min.
            time_15 = rate.get_data('first_request_of_the_last_15')
            time_15_ts = int(get_timestamp(time_15, "%Y-%m-%dT%H:%M:%SZ"))
            while time_15_ts + 950 > int(time.time()):
                print("wait 15 min to unlock api strava access")
                time.sleep(1)
        else:
            # the day test
            if not rate.get_data('quota_day') <= 990:
                # wait 1 day.
                first_req_day = rate.get_data('first_request_of_the_day')
                time_now = get_str_time(datetime.now())
                while first_req_day[0:10] == time_now[0:10]:
                    print("wait 1 day to unlock api strava access")
                    time.sleep(1)
            else:
                for segment in segments['segments']:
                    try:    
                        segment_info = strava.get_segment_by_id(segment['id'])
                        if "distance" not in segment_info:
                            print(f"could fetch distance for {segment_info['name']}")
                            continue
                        distance = segment_info['distance']
                        time = convert_time(segment_info['xoms']['kom'])
                        speed = convert_speed(time,distance,"km_h")
                        athlete_count = segment_info['athlete_count']
                        average_grade = segment_info['average_grade']
                                    
                        row = {
                            "id":segment_info['id'],
                            "feasibility": "yes" if (speed < 80 and athlete_count < 30000) else "no",
                            "speed_by_grade":speed / average_grade if average_grade else speed ,
                            "name":segment_info['name'],
                            "distance":distance,
                            "kom":time,
                            "speed":speed,
                            "average_grade":average_grade,
                            "maximum_grade":segment_info['maximum_grade'],
                            "elevation_high":segment_info['elevation_high'],
                            "elevation_low":segment_info['elevation_low'],
                            "climb_category":segment_info['climb_category'],
                            "created_at":segment_info['created_at'],
                            "updated_at":segment_info['updated_at'],
                            "total_elevation_gain":segment_info['total_elevation_gain'],
                            "effort_count":segment_info['effort_count'],
                            "athlete_count":athlete_count,
                            "star_count":segment_info['star_count'],
                            #"local_legend":segment_info['local_legend']['effort_count'] if "effort_count" in segment_info['local_legend'] else "none",
                            "local_legend":segment_info['local_legend']
                        }
                        rows.append(row)

                    except Exception as e: 
                        print(f"error fetching info for this segment: {e}")


    df = pd.DataFrame(rows)        
    ts = datetime.now().strftime("%Y%m%d%H%M%S")    
    output_file = f'reports/{ts}_{output_file}.csv'
    df.to_csv(output_file, sep='|', index=False)


if __name__ == '__main__':

    strava.access_token = strava.refresh(write=True)
        
    # Richmond park (uk)
    #coordinates = [51.3977365062017, -0.3089109797877128, 51.461489208009404, -0.2463514750273678 ]
    #generate_segments_report(output_file='richmond_segments.csv',coordinates=coordinates, step=1)

    # London (uk)
    coordinates = [51.2956935082215, -0.5569311506363874, 51.79255057165816, 0.4590442005871429 ]
    generate_segments_report(output_file='london_segments.csv',coordinates=coordinates, step=1)