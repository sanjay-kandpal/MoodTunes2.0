import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import random
import json
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="e0118b8dfe2a48da89544cb71f3928aa",
                                               client_secret="efa2bd088a064defb0fdbf238265accf",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-read-playback-state streaming ugc-image-upload playlist-modify-public"))

df1 = pd.read_csv('G:\eMO\MoodTunes\songRecommender\data\data_moods.csv')
fp=open(r'G:\eMO\MoodTunes\new.txt','r')
mood = fp.read()
fp.close()

df2 = df1.loc[df1['mood'] == mood]
df2 = df2.astype({'id':'string'})
list_of_songs=[]
for row in df2.iterrows():
    list_of_songs.append("spotify:track:"+str(row[1]['id']))
list_of_songs=random.sample(list_of_songs,15)
print(len(list_of_songs))
playlist_name = mood+' Songs'
playlist_description = mood+' Songs'
user_id = sp.me()['id']
sp.user_playlist_create(user=user_id,name=playlist_name,public=True,description=playlist_description)
prePlaylists = sp.user_playlists(user=user_id)
playlist = prePlaylists['items'][0]['id']
print(playlist)
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist, tracks=list(list_of_songs))
print("Created "+mood+" playlist")
fp=open(r'G:\eMO\MoodTunes\new.txt','w')
fp.write(playlist)
fp.close()
# After creating the playlist
token_info = sp.auth_manager.get_cached_token()
access_token = token_info['access_token']

# Write both the access token and playlist ID to the file
with open(r'G:\eMO\MoodTunes\new.txt', 'w') as fp:
    json.dump({'token': access_token, 'playlist': playlist}, fp)

import os
os.system(r'python G:\eMO\MoodTunes\songRecommender\test2.py')