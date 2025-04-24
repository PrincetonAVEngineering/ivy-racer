import requests

def send_data():
    # Define the URL of the receiver
    url = "http://10.49.248.230:5500/receive"

    # Data to send
    data = {
        "message": "Hello from transmitter!",
        "timestamp": "2025-04-24T12:00:00Z"
    }

    try:
        # Send a POST request with JSON data
        response = requests.post(url, json=data)

        # Print the response from the server
        print(f"Response: {response.status_code}, {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

if __name__ == '__main__':
    send_data()