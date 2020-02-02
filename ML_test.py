import pandas as pd
import csv
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from collections import defaultdict
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json.decoder import JSONDecodeError

client_id = "62ea08ff57004c409b395aeef8fc23cd"
client_secret = "6acf6c898c80405f8f4434b71755cf90"
client_redirect_uri = 'http://localhost:8888'
client_cred = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_cred)

fantano_file = './feature_ratings.csv'
fantano_data = pd.read_csv(fantano_file)
y = fantano_data.Score
# print('y', type(y))

fantano_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']
X = fantano_data[fantano_features]
# print('X', type(X))

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
# fantano_model = DecisionTreeRegressor(random_state=1)
# fantano_model.fit(train_X, train_y)

fantano_model = RandomForestRegressor(random_state=1, max_leaf_nodes=100)
fantano_model.fit(X, y)
# fantano_preds = fantano_model.predict(val_X)
# print("MAE:", mean_absolute_error(val_y, fantano_preds))

#here
while True:
    new_album = input("Enter an album ('get me out plz' to quit): ")
    if new_album == 'get me out plz':
        break

    album_id = sp.search(new_album, type = 'album', limit = 1)['albums']['items'][0]['id']
    album_name = sp.search(new_album, type = 'album', limit = 1)['albums']['items'][0]['name']
    album_artists = sp.search(new_album, type = 'album', limit = 1)['albums']['items'][0]['artists']

    album_file = './albums_rating.csv'

    csv_col = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']
    # album_csv = open(album_file, 'w', encoding = 'utf8')


    with open(album_file, 'w', encoding = 'utf8') as f:
        f.write("%s,%s,%s,%s,%s,%s,%s\n"%(csv_col[0], csv_col[1], csv_col[2], csv_col[3], csv_col[4], csv_col[5], csv_col[6]))
        csv_f = csv.reader(f)
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
        dictAvgFeat = {x:sum(y)/len(y) for x, y in dictAvgFeat.items()}
        f.write("%s,%s,%s,%s,%s,%s,%s\n"%(dictAvgFeat['acousticness'],dictAvgFeat['danceability'],dictAvgFeat['energy'],dictAvgFeat['instrumentalness'],dictAvgFeat['liveness'],dictAvgFeat['speechiness'],dictAvgFeat['valence']))

    # print(album_file)
    input_data = pd.read_csv(album_file)
    input_X = input_data[fantano_features]
    pred_score = fantano_model.predict(input_X)

    final_artists = [artist['name'] for artist in album_artists]
    print(album_name, "by", ', '.join(final_artists) + ":", pred_score[0])