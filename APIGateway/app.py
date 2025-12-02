from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Service URLs (internal Docker network)
CAR_CATALOG_SERVICE = "http://car-catalog-service:5002"


# Account Service routes
@app.route('/cars', methods=['GET'])
def getAllCars():
    #auth_header = request.headers.get('Authorization')
    #headers = {'Authorization': auth_header} if auth_header else {}
    #response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    response = requests.get(f"{CAR_CATALOG_SERVICE}/cars")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)