#api fields
runner_url = "https://www.strava.com/oauth/token"
refresh_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
laps_url_start = "https://www.strava.com/api/v3/activities/"
athlete_url = "https://www.strava.com/api/v3/athlete"
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
seconds_to_minutes = 1 / 60

meters_to_miles = 1 / 1609.34
meters_to_kilometers = 1 / 1000

cadence_multiplier = 2
pace_conversion_dict = {
    "Miles": 26.8223,
    "Kilometers": 16.6667
}

#lap types
lap_types = ["easy_distance", "lt1_distance", "lt2_distance", "hard_distance"]
formatted_lap_types = ["Easy Distance", "LT1 Distance", "LT2 Distance", "Hard Distance"]

#distance fields
distance_fields = ["easy_distance", "lt1_distance", "lt2_distance", "hard_distance", "activity_meters", "lap_meters"]

#base urls 
activity_base_url = "http://127.0.0.1:5000/activity/"

#default runner set up
default_preferred_unit = "Miles"
default_preferred_tracking = "Heartrate"
deafult_lt1 = 160
deafult_lt2 = 167
deafult_hard = 173

#unit dict
units_dict = {
    "Miles": "mi",
    "Kilometers": "km"
}

#dashboard
weeks_to_trend = 5

mileage_trend_axis = {
    "easy_distance": "Easy Distance",
    "lt1_distance": "LT1 Distance",
    "lt2_distance": "LT2 Distance",
    "hard_distance": "Hard Distance"
}

