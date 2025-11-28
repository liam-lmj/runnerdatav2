import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from .database_constants import runner_url, refresh_url, activities_url, laps_url_start, lap_url_end, page_limit
from .database_classes.activity import Activity
from .database_classes.lap import Lap
from .database_classes.runner import Runner

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def load_runner(code):
    response = requests.post(runner_url, params={"client_id": client_id, 
                                                 "client_secret": client_secret,
                                                 "code": code, 
                                                 "grant_type": "authorization_code"})
    
    if not response.ok:
        raise Exception("Failed get runner")
    
    response_json = response.json()
    refresh_token = response_json["refresh_token"]
    runner_id = response_json["athlete"]["id"]

    return refresh_token, runner_id

def new_access_token(refresh_token):
    response = requests.post(refresh_url, params={"client_id": client_id,
                                                  "client_secret": client_secret,
                                                  "refresh_token": refresh_token,
                                                  "grant_type": "refresh_token"})
    
    if not response.ok:
        raise Exception("Failed to refresh token")
    
    response_json = response.json()
    access_token = response_json["access_token"]

    return access_token

def update_activities(access_token):
    response = requests.get(activities_url, params={"access_token": access_token,
                                                    "per_page" : page_limit})
    
    if not response.ok:
        raise Exception("Failed to get activities data")
    
    response_json = response.json()
    
    for activity_dictionary in response_json:
        activity_id = activity_dictionary["id"]
        activity = Activity(activity_id, activity_dictionary)

        if not activity.exists and activity.valid:
            activity.set_activity_attributes(activity_dictionary)
            activity.add_to_database()
            update_laps(access_token, activity_id, activity.runner_id)

def update_laps(access_token, activity, runner_id):
    laps_url = laps_url_start + str(activity) + lap_url_end
    response = requests.get(laps_url, params={"access_token": access_token})

    if not response.ok:
        raise Exception("Failed to get lap data")
    
    response_json = response.json()

    runner = Runner(runner_id)

    for lap_dictionary in response_json:
        lap_id = lap_dictionary["id"]
        lap = Lap(lap_id, lap_dictionary, runner.runner_id, runner.prefered_tracking, runner.lt1, runner.lt2, runner.hard)
        lap.add_to_database()