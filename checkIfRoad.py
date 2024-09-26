import requests
from geopy.distance import great_circle

def is_point_on_road(lat, lon, radius=50):
    """
    Check if a point defined by latitude and longitude is on or near a road.

    Parameters:
    - lat: Latitude of the point
    - lon: Longitude of the point
    - radius: Distance in meters to consider as 'near' a road

    Returns:
    - bool: True if the point is on or near a road, False otherwise
    """
    # Define Overpass API query
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      way["highway"](around:{radius},{lat},{lon});
      relation["highway"](around:{radius},{lat},{lon});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        return len(data['elements']) > 0
    else:
        print("Error fetching data from Overpass API")
        return False

# Example usage
latitude = input()
longitude = input()

if is_point_on_road(latitude, longitude):
    print("The point is on a road.")
else:
    print("The point is not on a road.")