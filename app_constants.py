import os
from dotenv import load_dotenv

#strava auth url
load_dotenv()
client_id = os.getenv("client_id")
redirect_uri = os.getenv("redirect_uri")
auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read,activity:read_all&approval_prompt=force"