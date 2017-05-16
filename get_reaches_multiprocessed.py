import json
import multiprocessing
import requests
from roulettewheel import RouletteWheel

LASTFM_API_KEY = '053c2f4d20bda39f8e353be6e277d6d0'
LASTFM_SHARED_SECRET = '573e5a2995048342d40070134835c0e1'
TAG_GETINFO_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag={tag}&api_key={api_key}&format=json'


def get_tag_reach(tag):
    response = requests.get(TAG_GETINFO_URL.format(api_key=LASTFM_API_KEY, tag=tag))
    tag_info = json.loads(response.text)
    tag_reach = tag_info['tag']['reach']
    print("{genre}: {genre_reach}".format(genre=tag, genre_reach=tag_reach))
    return tag, tag_reach


# print(get_tag_reach("noise"))
if __name__ == '__main__':
    genres_rw = RouletteWheel()
    data = {}
    pool = multiprocessing.Pool()
    genres_reaches = pool.map(get_tag_reach, ((genre.rstrip(),) for genre in open('genres.txt') if
                                              not genre.startswith('#') and not genre.startswith('!')))
    pool.close()
    pool.join()
    genres_reaches = {genre: genre_reach for genre, genre_reach in genres_reaches}
    with open('genres_reaches_multiprocessed.json', 'w') as outfile:
        json.dump(data, outfile)