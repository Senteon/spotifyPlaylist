import requests
import json
from youtubesearchpython import VideosSearch

#   Required information to get an access token
authURL = 'https://accounts.spotify.com/api/token'

#   Base URL of all Spotify API endpoints
baseURL = 'https://api.spotify.com/v1/'

#   Have user input their client and secret info
#   TODO: Allow for users to login to spotify to get token
clientID = "5105ae150883408c96876a057fd39d16"
clientSecret = "2f1355ae51e94a7782f43b589cff61d4"
MAX_FETCH = 100



#   Create payload with proper information
payload = {}
payload['client_id'] = clientID
payload['client_secret'] = clientSecret
payload['grant_type'] = 'client_credentials'

#   Query token endpoint with payload and store response
authResponse = requests.post(authURL, payload)

#   Get response JSON
responseData = authResponse.json()

#   Save access token
accessToken = responseData['access_token']

#   Allow user to input playlist URL
playlistURL = ""
base = "https://open.spotify.com/playlist/"
while base not in playlistURL:
    playlistURL = input("Enter playlist URL: ")

#   Get relevant part of URL
splitL = playlistURL.split("playlist/")[1]
playlistID = splitL.split("?")[0]

#   Create header with our token
header = {'Authorization' : 'Bearer {}'.format(accessToken)}

#   Keep querying until all entries from playlist have been received
queryResult = requests.get(baseURL + 'playlists/' + playlistID + '/tracks' + '?fields=total&offset=0', headers = header)
tot = queryResult.json()['total']
offset = 0
customList = []

#   Read and create custom list out of query JSON
while (offset < tot):
    queryResult = requests.get(baseURL + 'playlists/' + playlistID + '/tracks' + '?fields=total,items(track(name, artists(name)))&offset={}'.format(offset), headers = header)
    for entry in queryResult.json()['items']:
        songEntry = [[],[]]
        for artist in entry['track']['artists']:
            songEntry[0].append(artist['name'])
        songEntry[1].append(entry['track']['name'])
        customList.append(songEntry)
    offset += MAX_FETCH

#   Use YoutubeSearch to find links for all songs and add to lists.
videosSearch = VideosSearch('', limit = 1)

for songEntry in customList:
    videosSearch.query = "{} {}".format(songEntry[0][0], songEntry[1][0])
    songEntry.append([videosSearch.result()['result'][0]['link']])




for songEntry in customList:
    print(songEntry)




