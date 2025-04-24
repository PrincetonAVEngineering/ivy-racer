from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receive', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Process the received data
    print(f"Received data: {data}")

    # Respond to the sender
    return jsonify({"success": "All Gucci"}), 200

@app.route('/test', methods=['GET'])
def test():
    return render_template("test.html")

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=5500)