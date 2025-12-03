from flask import Flask, request, jsonify, Response
import requests
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, get_jwt)
import os

app = Flask(__name__)

# Service URLs (internal Docker network)

services = {
    "car-catalog-service": "http://car-catalog-service:5002",
    "customer-support-service": "http://customer-support-service:5003/",
    "authorization-service": "http://authorization-service:5004"
}

CAR_CATALOG_SERVICE = "http://car-catalog-service:5002" # føles som noget som burde være i .env, specielt når det er med stort
CUSTOMER_SERVICE = "http://customer-support-service:5003/"
AUTHORIZATION_SERVICE = "http://authorization-service:5004" # "http://authorization-service:5004"

def getJWTPublicKey():
    url = f"{AUTHORIZATION_SERVICE}/getPublicKey"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        key = data.get("key")
        if key and isinstance(key, str):
            # Convert escaped newlines to real newlines
            key = key.encode('utf-8').decode('unicode_escape')
        print("Successfully retrieved JWT public key!")
        return key
    except Exception as e:
        print(f"ERROR getting JWT public key: {e}")
        return None

resp = requests.get("http://authorization-service:5004/getPublicKey")
PUBLIC_KEY = resp.json()["key"]

jwt = JWTManager(app)

# jwt auth config
# app.config["JWT_TOKEN_LOCATION"] = ["headers"] # hvor skal kigge for at finde auth
# app.config["JWT_HEADER_NAME"] = "Authorization"
# app.config["JWT_HEADER_TYPE"] = "Bearer" # skal stå bearer før jwt (standard måde at gøre på)
app.config["JWT_ALGORITHM"] = "RS256" # asymetrisk algoritme som kan testes af public men kun krypteres af secret
# app.config["JWT_DECODE_ALGORITHMS"] = ["RS256"]
app.config["JWT_PUBLIC_KEY"] = PUBLIC_KEY # public key kan bruges til at validere tokens, den får vi fra AuthorizationService


@app.route('/getAuthToken', methods=['POST'])
@jwt_required(optional=True)
def getAuthToken():
    url = f"{AUTHORIZATION_SERVICE}/getAuthToken"

    response = requests.request(
        method="POST",
        url=url,
        headers=dict(request.headers),
        data=request.get_data() # body hedder i flask data
    )

    data = response.json()

    return response.content



@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    auth = get_jwt()
    headers = request.headers
    return jsonify(msg="hello there")




@app.route('/<service>/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required(optional=True)
def lyskryds(service, path):

    url = f"{services[service]}/{path}"

    response = requests.request(
        method=request.method,
        url=url,
        headers=dict(request.headers), # vi omformaterer fordi req-headersne har formatet flak-header, men headers argumentet forventer dict
        params=request.args,
        data=request.get_data(),
    )

    clientResponse = Response(
        response=response.content, 
        status=response.status_code,
        headers=dict(response.headers)
        )

    return clientResponse


# Account Service routes
@app.route('/cars', methods=['GET'])
@jwt_required()
def getAllCars():
    #auth_header = request.headers.get('Authorization')
    #headers = {'Authorization': auth_header} if auth_header else {}
    #response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    response = requests.get(f"{CAR_CATALOG_SERVICE}/cars")
    return jsonify(response.json()), response.status_code

@app.route('/cars/query', methods=['GET'])
@jwt_required()
def queryCars():
    params = request.args.to_dict()
    response = requests.get(f"{CAR_CATALOG_SERVICE}/cars/query", params=params)
    return jsonify(response.json()), response.status_code

@app.route('/cars', methods=['POST'])
@jwt_required(optional=True)
def addCar():
    data = request.get_json(force=True)
    response = requests.post(f"{CAR_CATALOG_SERVICE}/cars", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/cars/stelnr/<stelNR>', methods=['PUT'])
@jwt_required(optional=True)
def getCarByStelNR(stelNR):
    data = request.get_json(force=True)
    response = requests.put(f"{CAR_CATALOG_SERVICE}/cars/stelnr/{stelNR}", json=data)
    return jsonify(response.json()), response.status_code



@app.route('/complaints', methods=['GET'])
@jwt_required(optional=True)
def getAllComplaints():

    # response = requests.get("http://customer-support-service:5003/complaints")

    response = requests.get(f"{CUSTOMER_SERVICE}/complaints")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)