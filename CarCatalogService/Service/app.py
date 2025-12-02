from flask import Flask, jsonify, request
from mongoengine import connect, Document, StringField, IntField

# adjust DB name if needed — your init script used "car-catalog-db"
# Use the compose service name for the DB host (car-catalog-db)
connect(db='car-catalog-db', host='car-catalog-db', port=27017)

app = Flask(__name__)

class Car(Document):
    make = StringField(required=True)
    model = StringField(required=True)
    year = IntField()
    stelNR = StringField(required=True)
    meta = {"collection": "cars"}

def car_to_dict(car):
    d = car.to_mongo().to_dict()
    d['id'] = str(d.pop('_id'))
    return d

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.objects()
    return jsonify([car_to_dict(c) for c in cars])

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
