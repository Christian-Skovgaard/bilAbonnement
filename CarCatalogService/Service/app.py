from flask import Flask, jsonify
from mongoengine import connect, Document, StringField, IntField

# adjust DB name if needed — your init script used "car-catalog-db"
# Use the compose service name for the DB host (car-catalog-db)
connect(db='car-catalog-db', host='car-catalog-db', port=27017)

app = Flask(__name__)

class Car(Document):
    make = StringField(required=True)
    model = StringField(required=True)
    year = IntField()
    meta = {"collection": "cars"}

def car_to_dict(car):
    d = car.to_mongo().to_dict()
    d['id'] = str(d.pop('_id'))
    return d

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.objects()
    return jsonify([car_to_dict(c) for c in cars])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)