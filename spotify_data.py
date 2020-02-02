import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json.decoder import JSONDecodeError
import csv
import pandas as pd


client_id = "62ea08ff57004c409b395aeef8fc23cd"
client_secret = "6acf6c898c80405f8f4434b71755cf90"
client_redirect_uri = 'http://localhost:8888'

client_cred = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_cred)
name = "Lover" #input
result = sp.search(name)
csv_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

#print(result['tracks']['items'][0]['album']['artists'][0]['id'])
# artist genre below
#print(sp.artist(result['tracks']['items'][0]['album']['artists'][0]['id'])['genres'])
#print(result['tracks']['items'][0]['album']['id'])
#print(sp.album(result['tracks']['items'][0]['album']['id'])['genres'])
#print(sp.audio_features([sp.album(result['tracks']['items'][0]['album']['id'])['tracks']['items'][x]['id'] for x in range(sp.album(result['tracks']['items'][0]['album']['id'])['total_tracks'])]))

csv_file = "AverageAudioFeature.csv"
dictAvgFeat = dict()
for tracks in sp.audio_features([sp.album(result['tracks']['items'][0]['album']['id'])['tracks']['items'][x]['id'] for x in range(sp.album(result['tracks']['items'][0]['album']['id'])['total_tracks'])]):
    for keys in tracks:
        if keys not in dictAvgFeat and keys in csv_columns:
            dictAvgFeat[keys] = [tracks[keys]]
        elif keys in csv_columns:
            dictAvgFeat[keys].append(tracks[keys])
dictAvgFeat = {x:sum(y)/len(y) for x, y in dictAvgFeat.items()}
with open(csv_file, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = csv_columns)
    writer.writeheader()
    writer.writerow(dictAvgFeat)

fantano_file = '../fantanoBot/fantano_ratings.csv'
with open(fantano_file, encoding = 'utf8') as f:
    csv_f = csv.reader(f)
    for i in csv_f:
        if i[1] != "Album":
            results = sp.search(i[1], type = 'album', limit = 1)
            print(results)




