from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b4b82f14a4154d98b5bee3e12eacabdd",
                                               client_secret="baef818bd54f402292d1d1d4d6bee160",
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

 
date = input('What year you would like to travel to (YYYY-MM-DD)?: ')
response = requests.get(url=f'https://www.billboard.com/charts/hot-100/{date}')
billboard_website = response.text

soup = BeautifulSoup(billboard_website, 'html.parser')
title_selector = '.o-chart-results-list-row-container .o-chart-results-list-row .lrv-u-width-100p .lrv-a-unstyle-list .o-chart-results-list__item h3'
hot_100_songs = [item.getText().strip() for item in soup.select(title_selector)]


user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False, description='')
song_uris = []
for song in hot_100_songs:
    result = sp.search(q=song, limit=1)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

