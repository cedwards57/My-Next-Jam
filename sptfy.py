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

def get_info():
    """ Grabs all the Spotify info needed for the page. Imported to app.py. """

    def get_releases():
        response = requests.get(BASE_URL + "browse/new-releases", headers=headers, params=params)
        response_json = response.json()

        releases = response_json["albums"]["items"]
        release_list = []
        for i in releases:
            release_list.append(i["name"])
        return release_list

    def get_artist_songs(artist):
        response = requests.get(BASE_URL + "artists/" + artist + "/albums", headers=headers)
        response_json = response.json()
        albums = response_json["items"]
        album_list = []

        for i in albums:
            album_list.append(i["id"])
        
        song_list = []
        for i in album_list:
            album_response = requests.get(BASE_URL + "albums/" + i + "/tracks", headers=headers)
            album_response_json = album_response.json()

            songs = album_response_json["items"]
            for j in songs:
                song_list.append(j["name"])

        return song_list
    
    artist_list = {
        "Marina": "6CwfuxIqcltXDGjfZsMd9A"
    }

    song_list = []
    for i in artist_list.values():
        song_list.extend(get_artist_songs(i))

    return {
        "releases": get_releases(),
        "songs": song_list
    }

get_info()
