from flask import Flask, jsonify, request
import pymongo
from bson import Regex

myclient = pymongo.MongoClient("mongodb://car-catalog-db:27017")
mydb = myclient["car-catalog-db"] # Choose database "car-catalog-db"
mycol = mydb["cars"] # Choose collection

app = Flask(__name__)

# Get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cursor = mycol.find({}, {"_id": 0}) # Query and remove MongoDB _id (surpress_id)
    cars = list(cursor)
    return jsonify(cars)

# Get queried cars
@app.route('/cars/query', methods=['GET']) # Skal kunne tage højde for, om pris er INDEN FOR monthlyMin og monthlyMax
def search_cars():
    queryParams = request.args # Dict of query parameters
    query = []

    for key, value in queryParams.items():      
        if value.lower() == ("true"): # Is boolean?
            query.append({key: True})
        elif value.lower() == ("false"):
            query.append({key: False})
        elif value.isdigit():
            query.append({key: int(value)})
        else: # Is string.
            if queryParams[key] != "": # Ignorerer parametre som "cars/query?regNr=&model="
                query.append({key: Regex(value, "i")})
        
    if query:
        mongo_filter = {"$and": query} # Request parameters given.
    else:
        mongo_filter = {}  # No request parameters given / empty request parameters like: ?brand=&model=

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    cars = list(cursor)
    return jsonify(cars)

#Get cars by kilometer range
@app.route('/cars/kilometer', methods=['GET'])
def get_cars_by_kilometer():
    min_km = request.args.get('min', type=int)
    max_km = request.args.get('max', type=int)

    mongo_filter = {
        "kmDriven": {
            "$gte": min_km,
            "$lte": max_km
        }
    }

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    cars = list(cursor)
    return jsonify(cars)

#Get cars by price range
@app.route('/cars/price', methods=['GET'])
def get_cars_by_price():
    min_price = request.args.get('min', type=int)
    max_price = request.args.get('max', type=int)

    mongo_filter = {
        "monthlyPrice": {
            "$gte": min_price,
            "$lte": max_price
        }
    }

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    cars = list(cursor)
    return jsonify(cars)


# Add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json(force=True)
    cursor = mycol.insert_one(data)
    # convert ObjectId to string for JSON serialization
    data['_id'] = str(cursor.inserted_id)
    return jsonify(data), 201

# Change car details by regNr
@app.route('/cars/<regNr>', methods=['PUT'])
def update_car(regNr):
    trimmedRegNr = regNr.strip(" ")  # Remove leading/trailing spaces
    data = request.get_json(force=True)
    car = mycol.find_one({"regNr": trimmedRegNr})
    if not car:
        return jsonify({"error": "Car not found"}), 404
    
    mycol.update_one({"regNr": trimmedRegNr}, {"$set": data})
    updated_car = mycol.find_one({"regNr": trimmedRegNr}, {"_id": 0})
    return jsonify(updated_car)

@app.route('/cars/<regNr>', methods=['DELETE'])
def delete_car(regNr):
    trimmedRegNr = regNr.strip(" ")  # Remove leading/trailing spaces
    car = mycol.find_one({"regNr": trimmedRegNr})
    if not car:
        return jsonify({"error": "Car not found"}), 404
    
    mycol.delete_many({"regNr": trimmedRegNr}) # delete_many bare lige, hvis der på mærkelig vis var flere biler med samme reg. nr.
    return jsonify("Car deleted.", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)