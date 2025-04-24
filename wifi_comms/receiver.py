from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Process the received data
    print(f"Received data: {data}")

    # Respond to the sender
    return jsonify({"message": "Data received successfully", "received_data": data}), 200

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=5500)