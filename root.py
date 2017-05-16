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

with open('genres_reaches.json') as infile:
    data = json.load(infile)
    for genre in data:
        genres_rw.add_variant(variant=genre, probability=data[genre])

print(genres_rw.get_choice())