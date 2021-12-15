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

def get_walking_data(access_token, user_id):
    url = "https://api.fitbit.com/1/user/" + user_id + "/activities/date/today.json"
    activity_request = requests.get(url, headers={"Authorization": "Bearer " + access_token})
    if activity_request.status_code==200:
        response = activity_request.json()['activities']
        print(response)
        if len(response)==0:
            return 0
        else:
            return int(response[0]['steps'])
            # return str("https://i.imgur.com/AtZtkic.jpg")

    else:
        print("Error while getting data\nError: " + str(activity_request.status_code))
    return False

def get_weight_log(access_token, user_id):
    url = "https://api.fitbit.com/1/user/" + user_id + "/body/weight/date/today/7d.json"
    activity_request = requests.get(url, headers={"Authorization": "Bearer " + access_token})
    if activity_request.status_code==200:
        response = activity_request.json()['body-weight']
        if len(response)==0:
            return 0
        else:
            return [i['value'] for i in response]
    else:
        print("Error while getting data\nError: " + str(activity_request.status_code))
    return False


def get_weight_vis(access_token, user_id):
    url = "https://api.fitbit.com/1/user/" + user_id + "/body/weight/date/today/7d.json"
    activity_request = requests.get(url, headers={"Authorization": "Bearer " + access_token})
    if activity_request.status_code==200:
        response = activity_request.json()['body-weight']
        print(response)
        if len(response)==0:
            return 0
        else:
            return [i['value'] for i in response]
    else:
        print("Error while getting data\nError: " + str(activity_request.status_code))
    return False


