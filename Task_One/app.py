from flask import Flask, jsonify, request
from utils import get_location, get_temperature

app = Flask(__name__)


"""Home route to test my flask app"""
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "HNG Internship Task One"}), 200



"""API Endpoint to get IP address, location and temparature"""
@app.route('/api/hello', methods=["GET"])
def greet_user():
    visitor_name = request.args.get('visitor_name', "Guest")
    if visitor_name.startswith("") and visitor_name.endswith(""):
        visitor_name = visitor_name[1:-2]

    """getting IP from the request header"""
    if 'X-Forwarded-For' in request.headers:
        headers = request.headers.get('X-Forwarded-For')
        client_ip = headers.split(',')[0]
        print(headers)
    
    else:
        client_ip = request.remote_addr

    """fuction to get location"""
    locations = get_location(client_ip)

    if isinstance(locations, list):
        """check temparature using city"""
        location = locations[0]
        temp = get_temperature(location)
        if temp == "Unknown temparature":
            """checking temparature using region"""
            location = locations[1]
            temp = get_temperature(locations[1])
    else:
        location = locations

    """function to get temparature"""
    
    """return json response"""
    return jsonify({
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temp} degrees Celcius in {location}"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")