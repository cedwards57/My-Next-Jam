import requests
import os
from dotenv import find_dotenv, load_dotenv
import random

load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GENIUS_AUTH_URL = "https://api.genius.com/oauth/authorize"
GENIUS_BASE_URL = "https://api.genius.com/"
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

auth_response = requests.post(AUTH_URL, {
    "grant_type": 'client_credentials',
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
})

auth_response_json = auth_response.json()
token = auth_response_json["access_token"]

headers = {
    "Authorization": str("Bearer " + token)
}

genius_headers = {
    "Authorization": str("Bearer " + GENIUS_TOKEN)
}

def get_info():
    """ Grabs all the Spotify & Genius info needed for the page. Imported to app.py. """

    def get_genius_url(query):
        """ Return a link to the first song lyrics result of a genius query. """
        try:
            genius_response = requests.get(GENIUS_BASE_URL + f"search?q={query}", headers=genius_headers)
            genius_response_json = genius_response.json()
            song_path = genius_response_json["response"]["hits"][0]["result"]["path"]
            return "https://genius.com" + song_path
        except KeyError:
            return "https://genius.com/Rick-astley-never-gonna-give-you-up-lyrics"

    def get_track_info(track_id):
        """ Return a dictionary of all necessary info for a single song. """

        try:
            response = requests.get(BASE_URL + "tracks/" + track_id, headers=headers)
            response_json = response.json()
            genius_url = get_genius_url(response_json["name"])

            track_info = {
                "name": response_json["name"],
                "album": response_json["album"]["name"],
                "album_id": response_json["album"]["id"],
                "artist": response_json["album"]["artists"][0]["name"],
                "artist_id": response_json["album"]["artists"][0]["id"],
                "image_url": response_json["album"]["images"][0]["url"],
                "preview_url": response_json["preview_url"],
                "genius_link": genius_url
            }
            return track_info
        except KeyError:
            return {
                "name": "Never Gonna Give You Up",
                "album": "Whenever You Need Somebody",
                "album_id": "6N9PS4QXF1D0OWPk0Sxtb4",
                "artist": "Rick Astley",
                "artist_id": "0gxyHStUsqpMadRV0Di1Qt",
                "image_url": "https://i.scdn.co/image/ab67616d0000b273255e131abc1410833be95673",
                "preview_url": None,
                "genius_link": "https://genius.com/Rick-astley-never-gonna-give-you-up-lyrics"
            }

    def get_random_track(album_id):
        """ Returns a random song ID from the given album. """

        try:
            response = requests.get(BASE_URL + "albums/" + album_id + "/tracks", headers=headers)
            response_json = response.json()
            songs = response_json["items"]

            random_song = random.choice(songs)
            random_song_id = random_song["id"]
            return random_song_id
        except KeyError:
            return "4uLU6hMCjMI75M1A2tKUQC"

    def get_random_album(artist_id):
        """ Returns a random album or single ID from the given artist. """
        params = {
            "include_groups": "album,single"
        }
        try:
            response = requests.get(BASE_URL + "artists/" + artist_id + "/albums", headers=headers, params=params)
            response_json = response.json()
            albums = response_json["items"]

            random_album = random.choice(albums)
            random_album_id = random_album["id"]
            return random_album_id
        except KeyError:
            return "6N9PS4QXF1D0OWPk0Sxtb4"

    my_artists = {
        "MARINA": "6CwfuxIqcltXDGjfZsMd9A",
        "The Hush Sound": "1RCoE2Dq19lePKhPzt9vM5",
        "The Family Crest": "44CB1c0W2h1XR2vB7AKpa7"
    }
    
    random_song = get_track_info(get_random_track(get_random_album(random.choice(list(my_artists.values())))))

    def get_artist_from_search(query):
        params = {
            "q": query,
            "type": "artist",
            "limit": 1
        }
        try:
            response = requests.get(BASE_URL + "search", headers=headers, params=params)
            response_json = response.json()
            artist_id = response_json["artists"]["items"][0]["id"]
            return artist_id
        except (KeyError, IndexError):
            return "0gxyHStUsqpMadRV0Di1Qt"
    
    query = "754urfyjhd" # change to user input
    random_song_from_input_artist = get_track_info(get_random_track(get_random_album(get_artist_from_search(query))))
    
    print(random_song_from_input_artist)
    
    return {
        "random_song": random_song,
        "random_song_output": random_song_from_input_artist
    }

get_info()
