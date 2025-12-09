from flask import Flask, jsonify, request
import pymongo
from bson import Regex
from datetime import datetime

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

@app.route('/cars/query', methods=['GET'])
def search_cars():
    queryParams = request.args
    filters = []

    # Generic field filters (booleans, ints, strings)
    for key, value in queryParams.items():
        if key in ["minKm", "maxKm", "minPrice", "maxPrice"]:
            continue  # handled separately below

        if value.lower() == "true":
            filters.append({key: True})
        elif value.lower() == "false":
            filters.append({key: False})
        elif value.isdigit():
            filters.append({key: int(value)})
        else:
            if value != "":
                filters.append({key: Regex(value, "i")})

    # Kilometer range filter
    min_km = request.args.get("minKm", type=int)
    max_km = request.args.get("maxKm", type=int)
    km_filter = {}
    if min_km is not None:
        km_filter["$gte"] = min_km
    if max_km is not None:
        km_filter["$lte"] = max_km
    if km_filter:
        filters.append({"kmDriven": km_filter})

    # Price range filter
    min_price = request.args.get("minPrice", type=int)
    max_price = request.args.get("maxPrice", type=int)
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filters.append({"monthlyPrice": price_filter})

    # Combine everything
    mongo_filter = {"$and": filters} if filters else {}

    cursor = mycol.find(mongo_filter, {"_id": 0})
    return jsonify(list(cursor))


# Add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json(force=True)

    # Check if regNr already exists
    existing_car = mycol.find_one({"regNr": data["regNr"]})
    if existing_car:
        return jsonify({
            "error": "Car with this regNr already exists",
            "regNr": data["regNr"]
        }), 409  # HTTP 409 Conflict

    # Insert into CarCatalog DB
    cursor = mycol.insert_one(data)

    # convert ObjectId to string for JSON serialization
    data["_id"] = str(cursor.inserted_id)

    # Build damage record payload (only required fields)
    damage_payload = {
        "regNr": data["regNr"],
        "car": data["brand"],
        "model": data["model"],
        "modelYear": data["modelYear"],
        "damage_status": "None",
        "date": str(datetime.utcnow().strftime("%Y-%m-%d"))
    }

    try:
        # Call DamageRegistrationService using regNr in URL
        regNr = data["regNr"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        resp = requests.post(
            f"http://localhost:5005/cases/{regNr}",
            json=damage_payload,
            headers=headers
        )
        print(resp.status_code, resp.text)
    except Exception as e:
        print(f"Failed to notify DamageRegistrationService: {e}")

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