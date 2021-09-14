import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"

auth_response = requests.post(AUTH_URL, {
    "grant_type": 'client_credentials',
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET")
})

auth_response_json = auth_response.json()
token = auth_response_json["access_token"]

headers = {
    "Authorization": str("Bearer " + token)
}

params = {
    "limit": 10
}

response = requests.get(BASE_URL + "browse/new-releases", headers=headers, params=params)

response_json = response.json()

def get_releases():
    releases = response_json["albums"]["items"]
    release_list = []
    for i in releases:
        release_list.append(releases[i]["name"])
    return {
        "releases": release_list
    }
