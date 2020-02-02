import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json.decoder import JSONDecodeError
import csv
import pandas as pd
from collections import defaultdict


client_id = "62ea08ff57004c409b395aeef8fc23cd"
client_secret = "6acf6c898c80405f8f4434b71755cf90"
client_redirect_uri = 'http://localhost:8888'

client_cred = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_cred)



#print(result['tracks']['items'][0]['album']['artists'][0]['id'])
# artist genre below
#print(sp.artist(result['tracks']['items'][0]['album']['artists'][0]['id'])['genres'])
#print(result['tracks']['items'][0]['album']['id'])
#print(sp.album(result['tracks']['items'][0]['album']['id'])['genres'])
#print(sp.audio_features([sp.album(result['tracks']['items'][0]['album']['id'])['tracks']['items'][x]['id'] for x in range(sp.album(result['tracks']['items'][0]['album']['id'])['total_tracks'])]))

# for tracks in sp.audio_features([sp.album(result['tracks']['items'][0]['album']['id'])['tracks']['items'][x]['id'] for x in range(sp.album(result['tracks']['items'][0]['album']['id'])['total_tracks'])]):
#     for features in tracks:
#         if features not in dictAvgFeat and features in csv_columns:
#             dictAvgFeat[features] = [tracks[features]]
#         elif features in csv_columns:
#             dictAvgFeat[features].append(tracks[features])
# dictAvgFeat = {x:sum(y)/len(y) for x, y in dictAvgFeat.items()}
# with open(csv_file, 'w') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames = csv_columns)
#     writer.writeheader()
#     writer.writerow(dictAvgFeat)

name = "Lover" #input
result = sp.search(name, type="album", limit=1)


fantano_file = './fantano_ratings.csv'
# csv_file = "AverageAudioFeature.csv"
csv_col = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

result_csv = open('featureAndGenre_ratings.csv', 'w', encoding = 'utf8')
avgGenre_csv = open('avg_genre.csv', encoding='utf8')

result_csv.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%("Artist","Album","Score", csv_col[0], csv_col[1], csv_col[2], csv_col[3], csv_col[4], csv_col[5], csv_col[6], "genre"))

with open(fantano_file, encoding = 'utf8') as f:
    csv_f = csv.reader(f)
    for entry in csv_f:
        if entry[1] != "Album":
            #collect the extracted info and put it into the table
            #same row as the album (not necessarily the same file)
            #album = album object (however that happens)
            # print(entry[1])
            if len(sp.search(entry[1], type = 'album', limit = 1)['albums']['items']) == 0:
                continue
            album_id = sp.search(entry[1], type = 'album', limit = 1)['albums']['items'][0]['id']

            #for track in album (this will probably be something in the json lol):
            #   extract audio features into some variables
            temp_tracklist = []
            dictAvgFeat = defaultdict(list)
            for tracknum in range(len(sp.album(album_id)['tracks']['items'])):
                temp_tracklist.append(sp.album(album_id)['tracks']['items'][tracknum]['id'])
            
            for track in sp.audio_features(temp_tracklist):
                if track is None:
                    continue
                for feature in track:
                    if feature in csv_col:
                        dictAvgFeat[feature].append(track[feature])
            # print(dictAvgFeat)
            dictAvgFeat = {x:sum(y)/len(y) for x, y in dictAvgFeat.items()}
            # print(dictAvgFeat)


            #after calculating audio features
            # csv_col = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']
            feature_csv.write("%s,%s,%s"%(entry[0],entry[1],entry[2]))
            feature_csv.write(",%s,%s,%s,%s,%s,%s,%s\n"%(dictAvgFeat['acousticness'],dictAvgFeat['danceability'],dictAvgFeat['energy'],dictAvgFeat['instrumentalness'],dictAvgFeat['liveness'],dictAvgFeat['speechiness'],dictAvgFeat['valence']))

            # this gets the avg genre score from artists
