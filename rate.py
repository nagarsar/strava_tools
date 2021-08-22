import datetime
import time
import json
from util import *



rate_limit_file = "json_objects/rate_limits.json"
default = {
    "daily_quota": 1000,
    "15_min_quota": 100,
    "quota_day": 0,
    "quota_15": 0,
    "first_request_of_the_day": get_str_time(datetime.now()),
    "first_request_of_the_last_15": get_str_time(datetime.now()),
    "limit_reached_day": False,
    "limit_reached_15": False
}


def update_rate_limits(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        res = set_quota(1)
        print(f"success: {res}")
    return wrapper


def get_data(param=None):
    with open(rate_limit_file, 'r') as json_file:
        data = json.load(json_file)
    if param:
        return data[param]
    return data


def verify_data(data):
    if not "daily_quota" in data:
        return False
    if not "15_min_quota" in data:
        return False
    if not "quota_day" in data:
        return False
    if not "quota_15" in data:
        return False
    if not "last_request" in data:
        return False
    if not "first_request_of_the_day" in data:
        return False
    if not "first_request_of_the_last_15" in data:
        return False
    if not "limit_reached_day" in data:
        return False
    if not "limit_reached_15" in data:
        return False
    return True


def set_quota(quota):
    data = default if not verify_data(get_data()) else get_data()
    time_now = get_str_time(datetime.now())
    time_now_ts = int(time.time())
    quota_day = data['quota_day']
    first_req_day = data['first_request_of_the_day']
    quota_15 = data['quota_15']
    time_15 = data['first_request_of_the_last_15']
    time_15_ts = int(get_timestamp(time_15, "%Y-%m-%dT%H:%M:%SZ"))

    if time_now_ts - time_15_ts > 900:
        quota_15 = 0
        time_15 = time_now

    if first_req_day[0:10] != time_now[0:10]:
        quota_day = 0
        first_req_day = time_now

    data.update({
        "last_request": time_now,
        "first_request_of_the_day": first_req_day,
        "first_request_of_the_last_15": time_15
    })

    # now check limits
    if quota_day + quota > data['daily_quota']:
        print("limit_reached for the day ...")
        data.update({"limit_reached_day": True})
        status=False
    else:
        if quota_15 + quota > data['15_min_quota']:
            print("limit_reached for the current 15 min slot ...")
            data.update({"limit_reached_15": True})
            status=False
        else:
            quota_day += quota
            quota_15 += quota
            data.update({
                "quota_day": quota_day,
                "quota_15": quota_15,
                "limit_reached_day": False,
                "limit_reached_15": False
            })

            if quota_day == data['daily_quota']:
                data.update({"limit_reached_day": True})
            if quota_15 == data['15_min_quota']:
                data.update({"limit_reached_15": True})

            status=True

    with open(rate_limit_file, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return status