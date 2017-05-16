import json
import operator
from pprint import pprint

with open('genres_reaches.json') as infile:
    data = json.load(infile)
    sorted_data = sorted(data.items(), key=operator.itemgetter(1))
    pprint(sorted_data)