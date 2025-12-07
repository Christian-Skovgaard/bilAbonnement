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

    # Insert into CarCatalog DB
    cursor = cars.insert_one(data)

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



'''
from flask import Flask, jsonify, request
from mongoengine import connect, Document, StringField, IntField

# adjust DB name if needed — your init script used "car-catalog-db"
# Use the compose service name for the DB host (car-catalog-db)
connect(db='car-catalog-db', host='car-catalog-db', port=27017)

app = Flask(__name__)

# Car Document Model
class Car(Document):
    make = StringField(required=True)
    model = StringField(required=True)
    year = IntField()
    stelNR = StringField(required=True)
    meta = {"collection": "cars"}

# Helper function to convert Car document to dictionary
def car_to_dict(car):
    d = car.to_mongo().to_dict()
    d['id'] = str(d.pop('_id'))
    return d


#Get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.objects()
    return jsonify([car_to_dict(c) for c in cars])

#Add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json(force=True)
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    stelNR = data.get('stelNR')
    car = Car(make=make, model=model, year=year, stelNR=stelNR)
    car.save()
    return jsonify(car_to_dict(car)), 201

#get cars by query parameters
@app.route('/cars/query', methods=['GET'])
def search_cars():
    # Get query parameters
    make = request.args.get('make')
    model = request.args.get('model')
    year = request.args.get('year')
    stelNR = request.args.get('stelNR')
    
    # Build filter query
    filters = {}
    if make:
        filters['make__icontains'] = make
    if model:
        filters['model__icontains'] = model
    if year:
        try:
            filters['year'] = int(year)
        except ValueError:
            return jsonify({"error": "year must be an integer"}), 400
    if stelNR:
        filters['stelNR__icontains'] = stelNR
    
    # Query database
    cars = Car.objects(**filters)
    return jsonify([car_to_dict(c) for c in cars])
    return jsonify("Hi :3")

#Change car details by stelNR
@app.route('/cars/stelnr/<stelNR>', methods=['PUT'])
def update_car(stelNR):
    data = request.get_json(force=True)
    car = Car.objects(stelNR=stelNR).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404
    
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.stelNR = data.get('stelNR', car.stelNR)
    car.save()
    return jsonify(car_to_dict(car))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
'''