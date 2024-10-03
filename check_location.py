import requests
import os
from find_location import get_coordinates

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

location = get_coordinates()
lat = location[0]
long = location[1]
url = f'https://roads.googleapis.com/v1/nearestRoads?points={lat}%2C{long}&key={API_KEY}'
print(lat)
print(long)
r = requests.get(url, auth=('user', 'pass'))

results = r.json()
print(results["snappedPoints"][0]["location"])

new_long, new_lat = results["snappedPoints"][0]["location"]["longitude"], results["snappedPoints"][0]["location"]["latitude"]

print(new_lat)
print(new_long)
