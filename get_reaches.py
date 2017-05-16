import json
import requests
from roulettewheel import RouletteWheel

LASTFM_API_KEY = '053c2f4d20bda39f8e353be6e277d6d0'
LASTFM_SHARED_SECRET = '573e5a2995048342d40070134835c0e1'
TAG_GETINFO_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag={tag}&api_key={api_key}&format=json'


def get_tag_reach(tag):
    response = requests.get(TAG_GETINFO_URL.format(api_key=LASTFM_API_KEY, tag=tag))
    tag_info = json.loads(response.text)
    return tag_info['tag']['reach']


genres_rw = RouletteWheel()
data = {}
for genre in (genre.rstrip() for genre in open('genres.txt') if
              not genre.startswith('#') and not genre.startswith('!')):
# for genre in (genre.rstrip() for genre in open('genres.txt')):
#     if genre.startswith('#') or genre.startswith('!'):
#         genre = genre[2:]
    genre_reach = get_tag_reach(genre)
    print("{genre}: {genre_reach}".format(genre=genre, genre_reach=genre_reach))
    data[genre] = genre_reach
with open('genres_reaches.json', 'w') as outfile:
    json.dump(data, outfile)
