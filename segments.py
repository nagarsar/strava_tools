import strava
from util import *
import pandas as pd


# INFO : This function is very extensive in terms of API usage
#        TODO : possibility to run a job accros several days. 


def generate_segments_report(output_file="strava_template.csv",coordinates=[], step=0):
    """
    inputs:
     - output filename
     - coordinates of the area to cover
     - step : distance in km for intermediates areas in the area to cover, 0 to disable
    outputs:
     - csv file : ts_<output_file>
    return (None)
    """
    rows=[]
    if not coordinates:
        coordinates = [36.0, -94.1, 36.1, -94.0]
   
    all_coordinates=[]
    all_coordinates.append(coordinates)
    distance = get_distance(coordinates)     # km
    
    print(f"Given area: {distance[0]}km, | Step: {step}km")

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
    output_file = f'{ts}_{output_file}.csv'
    df.to_csv(output_file, sep='|', index=False)


if __name__ == '__main__':

    access_token = strava.refresh(write=True)
        
    # Richmond park (uk)
    #coordinates = [51.3977365062017, -0.3089109797877128, 51.461489208009404, -0.2463514750273678 ]
    #generate_report(output_file='richmond_segments.csv',coordinates=coordinates, step=1)

    # London (uk)
    coordinates = [51.2956935082215, -0.5569311506363874, 51.79255057165816, 0.4590442005871429 ]
    generate_segments_report(output_file='london_segments.csv',coordinates=coordinates, step=1)