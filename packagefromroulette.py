import json
from roulettewheel import RouletteWheel
packages = None
with open('pypiranking.json') as infile:
    packages = json.load(infile)['packages']
packages_rw = RouletteWheel()
for package in packages:
    packages_rw.add_variant(variant=package, probability=packages[package])
print('Your choice is the package known as "{title}"'.format(title=packages_rw.get_choice()))