import requests
from find_location import get_coordinates

location = get_coordinates()
lat = location[0]
long = location[1]
url = 'https://roads.googleapis.com/v1/nearestRoads?points='+str(lat)+'%2C'+str(long)+'&key=AIzaSyAbxTKktcXZ0iNWrJi_xQwtTikAJrkrfE4'
print(lat)
print(long)
r = requests.get(url, auth=('user', 'pass'))

results = r.json()
print(results["snappedPoints"][0])
