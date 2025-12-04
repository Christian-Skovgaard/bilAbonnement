from flask import Flask, request, jsonify, Response
import requests
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, get_jwt)
import os

# Service URLs (internal Docker network)
services = {
    "car-catalog-service": "http://car-catalog-service:5002",
    "customer-support-service": "http://customer-support-service:5003/",
    "authorization-service": "http://authorization-service:5004",
    "customer-managment-service": "temp:5005",
    "subscription-managment-service": "temp:5006",
    "payment-service": "temp:5007",
    "subscription-management-service": "http://subscription-management-service:5008"
}

app = Flask(__name__)
jwt = JWTManager(app)

resp = requests.get("http://authorization-service:5004/getPublicKey")
PUBLIC_KEY = resp.json()["key"]

# jwt auth config
app.config["JWT_ALGORITHM"] = "RS256" # asymetrisk algoritme som kan valideres af public men kun krypteres af private
app.config["JWT_PUBLIC_KEY"] = PUBLIC_KEY # public key kan bruges til at validere tokens, den får vi fra AuthorizationService


@app.route('/getAuthToken', methods=['POST'])
@jwt_required(optional=True)
def getAuthToken():
    url = f"{services['authorization-service']}/getAuthToken"

    response = requests.request(
        method="POST",
        url=url,
        headers=dict(request.headers),
        data=request.get_data() # body hedder i flask data
    )

    data = response.json()

    return response.content

#endpoint der hjælper med at teste om vi for svar
@app.route('/heath', methods=['GET'])
@jwt_required(optional=True)
def test():
    return jsonify(heath="tip top form 🏋️")


@app.route('/<service>/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required(optional=True)
def lyskryds(service, path):

    if not service in services:
        return jsonify(msg="no service with that name")

    url = f"{services[service]}/{path}"

    serviceResponse = requests.request(
        method=request.method,
        url=url,
        headers=dict(request.headers), # vi omformaterer fordi req-headersne har formatet flak-header, men headers argumentet forventer dict
        params=request.args,
        json=request.get_json(),
    )

    clientResponse = Response(
        response=serviceResponse.content, 
        status=serviceResponse.status_code,
        headers=dict(serviceResponse.headers)
        )

    return clientResponse




'''
# Account Service routes
@app.route('/cars', methods=['GET'])
@jwt_required(optional=True)
def getAllCars():
    #auth_header = request.headers.get('Authorization')
    #headers = {'Authorization': auth_header} if auth_header else {}
    #response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    response = requests.get(f"{CAR_CATALOG_SERVICE}/cars")
    return jsonify(response.json()), response.status_code

@app.route('/cars/query', methods=['GET'])
@jwt_required(optional=True)
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
'''
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)