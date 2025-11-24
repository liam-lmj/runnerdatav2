from stravaapi import load_runner, new_access_token, update_activities, update_laps

refresh_token = "d3ada2337d0eb912fd8538fe8a54a308e55a1bf7"

access_token = new_access_token(refresh_token)
response = update_activities(access_token)