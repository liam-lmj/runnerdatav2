#api fields
runner_url = "https://www.strava.com/oauth/token"
refresh_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
laps_url_start = "https://www.strava.com/api/v3/activities/"
lap_url_end = "/laps"

#max number of new activities per runner
page_limit = 25 

#days of week
day_map = {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "0": "Sunday"
}

#allowed activity types
valid_activity_types = ["Run"]

#conversions
seconds_to_hours = 1 / 3600

#lap_types
lap_types = ["easy_distance", "lt1_distance", "lt2_distance", "hard_distance"]