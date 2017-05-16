import requests
import json
from pprint import pprint

LASTFM_API_KEY = '053c2f4d20bda39f8e353be6e277d6d0'
LASTFM_SHARED_SECRET = '573e5a2995048342d40070134835c0e1'
ARTIST_GETINFO_URL = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={api_key}&format=json'
TAG_GETINFO_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag={tag}&api_key={api_key}&format=json'
USER_GETTOPARTISTS_URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={user}&api_key={api_key}&format=json&limit=1000&page={page}'
USERNAME = 'UNDEADUM'
genres = []
total_pages = None
artists = []
page = 1


def get_artist_genres(artist):
    artist = artist.replace('&', '%26')
    response = requests.get(ARTIST_GETINFO_URL.format(artist=artist, api_key=LASTFM_API_KEY))
    # print(response.url)
    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        pprint(response.text)
        return []
    # pprint(data)
    try:
        return [genre['name'].lower() for genre in data['artist']['tags']['tag'] if genre['name'].lower() != artist][:2]
    except KeyError as e:
        print(ARTIST_GETINFO_URL.format(artist=artist, api_key=LASTFM_API_KEY))
        pprint(data)
        return []

while total_pages is None or page < total_pages:
    response = requests.get(USER_GETTOPARTISTS_URL.format(user=USERNAME, api_key=LASTFM_API_KEY, page=page))
    data = json.loads(response.text)
    if total_pages is None:
        total_pages = int(data['topartists']['@attr']['totalPages'])
    for artist in data['topartists']['artist']:
        artist_genres = get_artist_genres(artist['name'])
        print(artist['name'], *artist_genres)
        genres.extend(artist_genres)
    page += 1

genres = list(set(genres))

with open('genres_undeadum.json', 'w') as outfile:
    json.dump(genres, outfile)