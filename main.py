import requests
import json

#   Required information to get an access token
authURL = 'https://accounts.spotify.com/api/token'

#   Base URL of all Spotify API endpoints
baseURL = 'https://api.spotify.com/v1/'

#   Have user input their client and secret info
#   TODO: Allow for users to login to spotify to get token

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
    queryResult = requests.get(baseURL + 'playlists/' + playlistID + '/tracks' + '?fields=total,items(track(external_urls))&offset={}'.format(offset), headers = header)
    for entry in queryResult.json()['items']:
        songEntry = ""
        songEntry = entry['track']['external_urls']['spotify']
        customList.append(songEntry)
    offset += MAX_FETCH


for songEntry in customList:
    print(songEntry)




