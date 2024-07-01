from flask import Flask, jsonify, request
from utils import get_location, get_temperature

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "HNG Internship Task One"}), 200

@app.route('/api/hello', methods=["GET"])
def greet_user():
    visitor_name = request.args.get('visitor_name', "Guest")

    if 'X-Forwarded-For' in request.headers:
        headers = request.headers.get('X-Forwarded-For')
        client_ip = headers.split(',')[0]
    
    else:
        client_ip = request.remote_addr
        headers = None
    location = get_location(client_ip)
    temp = get_temperature(location)
    return jsonify({
        "client_ip": client_ip,
        "location": location,
        "headers": headers,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temp} degree Celcius in {location}"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")