# fantanoBot

based on genres (he really likes indy music/weird music), artists (identity)
ENDGOAL: create a ML bot that can somewhat accurately rate albums, like da boi, Anthony Fantano

from spotify we can pull:
    ~~-genre(s) of each album~~
    ~~-maybe look into audio features object (danceability, energy, etc)~~
        -try finding a track we know well and see how it stacks up

from the spreadsheet:
    scores
    album names
    artist names
    (most importantly correlation between scores and genres/artists)

what do we need to extrapolate (to train model):
    ~~album genre (spotify data)~~
    avg audio features of the album (danceability, energy, etc)

suggestions:
    -right now model seems to only gravitate towards range of 4-7 instead of 1-10
        -incorporate genre bias
        -popularity normalization (from AI guys, incorporate popularity by dividing some stat or something like that lol)
        -only use the most popular songs on the album(?) [just not all of them lol]
    -find a way to get result stats (find the std dev to test model further)

# MAKING THIS WORK:
-input for the album (show search results from spotify and the user can pick)
    - extrapolate the information the model needs (genre, audio features [from each track])
        (it already has correlation between scores and both genres and artists)
    -https://stackoverflow.com/questions/11747527/how-to-connect-javascript-to-python-sharing-data-with-json-format-in-both-ways
-output a score
-train a model!!!! that does this for us
    -seikit
    -keras
    -mongoDB (put 2018 data into mongo [including genres/audio features])