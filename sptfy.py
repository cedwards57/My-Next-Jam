import requests
import os
from dotenv import find_dotenv, load_dotenv
import random

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

def get_info():
    """ Grabs all the Spotify info needed for the page. Imported to app.py. """

    def get_releases():
        """ Returns the latest 10 Spotify releases. """
        params = {
            "limit": 10
        }
        response = requests.get(BASE_URL + "browse/new-releases", headers=headers, params=params)
        response_json = response.json()

        releases = response_json["albums"]["items"]
        release_list = []
        for i in releases:
            release_list.append(i["name"])
        return release_list

    def get_albums(artist_id):
        params = {
            "include_groups": "album,single"
        }
        response = requests.get(BASE_URL + "artists/" + artist_id + "/albums", headers=headers, params=params)
        response_json = response.json()
        albums = response_json["items"]
        album_list = []

        for i in albums:
            album_list.append((i["id"],i["name"]))
        return album_list

    def get_all_songs(artist,album_list):
        """ Returns a list of dicts of all the current artist's songs """
        song_list = []
        for i in album_list:
            song_list.extend(get_album_songs(artist,i))
        return song_list
    
    def get_album_songs(artist,album):
        """ Returns a list of dicts about each song in the given album. """
        album_response = requests.get(BASE_URL + "albums/" + album[0] + "/tracks", headers=headers)
        album_response_json = album_response.json()
        songs = album_response_json["items"]

        album_songs = []
        for j in songs:
            this_song = {"name": j["name"], "id": j["id"], "artist": artist, "album": album[1]}
            album_songs.append(this_song)

        return album_songs

    def get_artist_songs(artist,artist_id):
        """ Returns a list of dictionaries with the name, artist, album, and ID of every song by the specified artist. Includes artist field because it gets compiled into a larger list with more artists later."""
        return get_all_songs(artist,get_albums(artist_id))
    
    # Takes a dictionary of artists and returns a list of dictionaries identifying ALL the songs between them.
    artist_list = {
        "MARINA": "6CwfuxIqcltXDGjfZsMd9A",
        "The Hush Sound": "1RCoE2Dq19lePKhPzt9vM5",
        "The Family Crest": "44CB1c0W2h1XR2vB7AKpa7"
    }
    all_song_list = []
    for i in artist_list:
        all_song_list.extend(get_artist_songs(i,artist_list[i]))

    return {
        "releases": get_releases(),
        "all_songs": all_song_list
    }

# change structure to artist: albums: songs
