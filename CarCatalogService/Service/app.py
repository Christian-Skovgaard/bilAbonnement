from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://car-catalog-db:27017")
print("Databases before connection")
print(myclient.list_database_names())

mydb = myclient["car-catalog-db"] # Choose database "car-catalog-db"


print(mydb.list_collection_names())

mycol = mydb["cars"] # Choose collection

print(mydb.list_collection_names())

app = Flask(__name__)

# Get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cursor = mycol.find({}, {"_id": 0}) # Query and remove MongoDB _id (surpress_id)
    cars = list(cursor)
    return jsonify(cars)

# Get queried cars
@app.route('/cars/query', methods=['GET'])
def search_cars():
    queryParams = request.args # Dict of query parameters
    query = []
    for key, value in queryParams.items():
        if value != "":
            query.append({key: value}) # Lav en liste af objekter til query ud fra query params f.eks.: [{brand : "Toyota"}, {model : "GT86"}]

    cursor = mycol.find({
       "$and": query
    }, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    cars = list(cursor)
    return jsonify(cars)


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