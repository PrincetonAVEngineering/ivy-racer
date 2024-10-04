import googlemaps
import pprint
import requests

def get_coordinates(address, api_key):
    # Format the URL for the request
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        # Extract latitude and longitude
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print("Error:", data['status'])
        return None

def coordsToPath(client, start_coordinates, end_coordinates):
    
    # Define origin and destination coordinates
    origin = start_coordinates  # (latitude, longitude)
    destination = end_coordinates  # (latitude, longitude)

    # Request directions via driving mode
    directions_result = client.directions(origin, destination, mode="walking")

    # Pretty-print the results to see the detailed directions
    pprint.pprint(directions_result)

    # Extract the route's path
    route = directions_result[0]['legs'][0]['steps']

    # Extract start and end locations for each step in the path
    path = [(step['start_location']['lat'], step['start_location']['lng']) for step in route]

    # Optionally, include the destination as the last point
    path.append((directions_result[0]['legs'][0]['end_location']['lat'], 
                directions_result[0]['legs'][0]['end_location']['lng']))

    print(f"Path between the two points: {path}")

# Example usage
api_key = 'YOUR_API_KEY'
start_address = '35 Palmer Square W, Princeton, NJ'
end_address = '48 Leavitt Lane, Princeton, NJ'

start_coords = get_coordinates(start_address, api_key)
end_coords = get_coordinates(end_address, api_key)

#if coordinates:
#    print("Coordinates:", coordinates)

# Initialize the client with your API key
gmaps = googlemaps.Client(key=api_key)

coordsToPath(gmaps, start_coords, end_coords)

