import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json.decoder import JSONDecodeError
import csv


client_id = "62ea08ff57004c409b395aeef8fc23cd"
client_secret = "6acf6c898c80405f8f4434b71755cf90"
client_redirect_uri = 'http://localhost:8888'

client_cred = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_cred)

# result = sp.search("Taylor Swift", type="artist", limit=1)
# print(result['artists']['items'][0]['genres'])

class GenreStats():
    def __init__(self, totalScore, albumCount):
        self.totalScore = totalScore
        self.albumCount = albumCount

    def __repr__(self):
        return f'Total Score: {self.totalScore}, Album Count: {self.albumCount}'

genreDict = {}
fantano_file = '../fantanoBot/fantano_ratings.csv'
with open(fantano_file, encoding="utf8") as f:
    csv_f = csv.reader(f)
    for row in csv_f:
        if row[0] == 'Artist':
            continue
        for artist in row[0].split(', '):

            spotResult = sp.search(artist, type="artist", limit=1)
            if len(spotResult['artists']['items']) == 0:
            	# print(artist, '  no search results')
            	continue
            # print(artist)
            # print(artist, spotResult['artists']['items'][0]['genres'])
            for genre in spotResult['artists']['items'][0]['genres']:
            	if genre not in genreDict:
            		genreDict[genre] = GenreStats(int(row[2]), 1)
            	else:
            		genreDict[genre].totalScore += int(row[2])
            		genreDict[genre].albumCount += 1


# for genre in genreDict:
# 	print(genre, ": ", genreDict[genre])

with open('avg_genre.csv', 'w') as f:
	f.write("%s,%s,%s\n"%("Genre", "TotalScore", "Album Count"))
	for genre in genreDict:
		f.write("%s,%i,%i\n"%(genre, genreDict[genre].totalScore, genreDict[genre].albumCount))