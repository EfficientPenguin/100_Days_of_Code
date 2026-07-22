'''
    This application scrapes the Billboard 100 site via Appbrewery alternative for the top 100 
    song titles for a specific month/year and builds a Spotify playlist with those songs -- pretty cool!
'''

import datetime as dt
import os
import json

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Constants
REDIRECT_URI = "http://127.0.0.1:1234"
TEST_PLAYLIST_ID = "YOUR-PLAYLIST-ID"
SONGS_NOT_ADDED_FILE = "not_on_spotify.txt"

# Load the environment variables from the .env file
load_dotenv()

# URL = "https://www.billboard.com/charts/hot-100/"

# Prompt user for the year they want the songs for in YYYY-MM-DD
# year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
sample_year = "2026-04-18"
URL = f"https://appbrewery.github.io/bakeboard-hot-100/{sample_year}/"

# Get the html page using requests
response = requests.get(url=URL)
response.raise_for_status()

# Make soup of the response.text
soup = BeautifulSoup(response.text, "html.parser")

# Get the songs and artists in h3 and span
songs = soup.select(selector=".chart-entry__info")

# Get the songs and artists as lists
artists_list = [song.span.getText() for song in songs]
songs_list = [song.h3.getText() for song in songs]

# Spotipy and Spotify section
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENT_ID"),
                                               client_secret=os.environ.get("CLIENT_SECRET"),
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True))

# 4. Fetch the authenticated user's ID
user_info = sp.current_user()
user_id = sp.current_user()["id"]
print(f"Authenticated successfully as: {user_info['display_name']} and {user_id}")

# # Create a playlist
# new_playlist = sp.current_user_playlist_create(name="TEST", public=True, description="A test playlist created using Python script.")
# playlists = sp.current_user_playlists(limit=50, offset=0)

# print(new_playlist)

# with open(file='playlists.json', mode='w') as file:
#     json.dump(new_playlist, file, indent=4)

# To hold song uris
items = []
songs_not_added = []

# Go through each song and artist in the list
for song,artist in zip(songs_list, artists_list):
    song_uri = None

    # Split it up by space
    track_list = song.split(' ')
    a_list = artist.split(' ')

    # SONGS ---- Build str and add %20 in place of space
    track = "%20".join(track_list)
    track += "%20"
    
    # ARTISTS --- Build str and add %20 in place of space
    a_encoded = "%20".join(a_list)

    q = f"remaster%20track:{track}artist:{a_encoded}"

    # Execute the query
    search_result = sp.search(q=q, limit=5, offset=0, type="track")
    # print(search_result)


    # Get a song from the search results and POST it to the playlist
    if len(search_result['tracks']['items']) == 0:
        continue
    else:
        song_uri = search_result['tracks']['items'][0]['uri']
    
    # Write song to playlist if it exists
    if song_uri != None:
        items.append(song_uri)
    else:
        songs_not_added.append(f"{song}, {artist}")

# Write the songs to the TEST playlist
add_items_result = sp.playlist_add_items(playlist_id=TEST_PLAYLIST_ID, items=items)

# Write missing songs to a file
with open(file=SONGS_NOT_ADDED_FILE, mode="w") as file:
    for item in songs_not_added:
        file.write(item)

# print()
# print(song_uri)

# Add song to the playlist


# add_items_result = sp.playlist_add_items(playlist_id=TEST_PLAYLIST_ID, items=[song_uri])
# print(add_items_result)

# with open(file="search_results.json", mode="w") as file:
#     json.dump(search_result, file, indent=4)




