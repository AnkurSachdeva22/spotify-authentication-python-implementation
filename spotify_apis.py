import requests
import requests.auth
import os
from urllib.parse import parse_qs, urlparse
import base64

# Add SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET in environment variables
# CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
# CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
# Or for testing add them here ID and SECRET. Change code below accordingly
ID = 'ADD YOUR API ID HERE'
SECRET = 'ADD API SECRET HERE'
BASE_URL = 'https://accounts.spotify.com'
AUTHORIZE_ENDPOINT = '/authorize'
TOKEN_ENDPOINT = '/api/token'
REDIRECT_URI = 'https://spotify.com/'
API_URL = 'https://api.spotify.com/v1'

class Spotify:
    def __init__(self):
        self.auth_request_parameter = {
            'client_id': ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'state': 'state',
            'scope': 'playlist-modify-public playlist-modify-private'
        }
        self.token_request_headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(f'{ID}:{SECRET}', 'utf-8')).decode('utf-8')}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.access_token = None
        self.id = None

    def authenticate(self):
        '''This method authennticates the user using cliend id in 3 steps. First it makes get request to get a code,
        then it gets the code out of the url, and then it makes a post request using the code, client id and client
        secret, and receives the token in current object\'s access_token attribute.'''

        # STEP 1: get 'code' using ' /authorize ' endpoint
        authorize_response = requests.get(url=f"{BASE_URL}{AUTHORIZE_ENDPOINT}", params=self.auth_request_parameter)
        print(authorize_response.status_code)
        authorize_response.raise_for_status()
        print(f"Go here to authorise: {authorize_response.url}")

        # STEP 2: parse the url to get 'code' and 'state'
        authorized_url = input("Enter the url: ")
        parsed_url = urlparse(authorized_url)
        print(parsed_url)
        code = parse_qs(parsed_url.query)['code'][0]
        state = parse_qs(parsed_url.query)['state'][0]
        print(code, state)

        # STEP 3: Use the code with ' /api/token ' endpoint
        token_request_body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }
        token_response = requests.post(url=f"{BASE_URL}{TOKEN_ENDPOINT}",
                                       headers=self.token_request_headers,
                                       params=token_request_body)
        print(token_response.text)
        token_response.raise_for_status()
        self.access_token = token_response.json()['access_token']
        print(token_response.json()['access_token'])

    def get_profile(self):
        '''This method uses token to get user\'s profile, and gets user id out of the response received.'''
        header = {
            'Authorization': f'Bearer {self.access_token}'
        }
        endpoint = '/me'
        response = requests.get(url=f"{API_URL}{endpoint}", headers=header)
        print(response.text)
        response.raise_for_status()
        print(response.status_code)
        self.id = response.json()['id']

    def create_playlist(self, playlist_name):
        endpoint = f'/users/{self.id}/playlists'
        name = playlist_name
        header = {
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {
            'name': name,
            'description': 'Created with code',
            'public': 'True'
        }
        response = requests.post(url=f"{API_URL}{endpoint}", headers=header, json=body)
        print(response.text)
        response.raise_for_status()
        return response.json()['id']

    def search(self, song):
        '''This method takes a string as input parameter, then searches the string using /search endpoint and
        access token. Finally returns the song\'s uri.'''
        endpoint = '/search'
        header = {
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {
            'q': song,
            'type': 'track',
            'limit': 10,
            'market': 'IN'
        }
        response = requests.get(url=f"{API_URL}{endpoint}", headers=header, params=body)
        # print(response.text)
        response.raise_for_status()
        print(f"uri for {song}: {response.json()['tracks']['items'][0]['uri']}")
        return response.json()['tracks']['items'][0]['uri']

    def add_song_to_list(self, id, songs):
        endpoint = f"/playlists/{id}/tracks"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {
            'uris': songs,
            'position': 0
        }
        add_song_response = requests.post(url=f"{API_URL}{endpoint}", headers=headers, json=body)
        print(add_song_response.text)
        add_song_response.raise_for_status()
        if add_song_response.status_code == 200:
            print("Songs added to playlist")

