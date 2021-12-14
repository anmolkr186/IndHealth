import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def call_authorization_url():
    url = os.environ.get("authotize_url", "")
    url += "?client_id=" + os.environ.get("client_id", "")
    url += "&response_type=token"
    url += "&redirect_uri=" + os.environ.get("redirect_uri", "")
    url += "&scope=" + os.environ.get("scope", "")
    url += "&expires_in=" + os.environ.get("expires_in", "")
    return url

def get_walking_data(acess_token, user_id):
    url = "https://api.fitbit.com/1/user/" + user_id + "/activities/date/today.json"
    activity_request = requests.get(url, headers={"Authorization": "Bearer " + acess_token})
    if activity_request.status_code==200:
        response = activity_request.json()['activities']
        if len(response)==0:
            return 0
        else:
            return int(response[0]['steps'])
    else:
        print("Error while getting data\nError: " + str(activity_request.status_code))
    return False