from flask import Flask, jsonify
from mongoengine import connect, Document, StringField, IntField

# adjust DB name if needed — your init script used "car-catalog-db"
# Use the compose service name for the DB host (car-catalog-db)
connect(db='customer-service-db', host='customer-service-db', port=27017)

app = Flask(__name__)

class Complaint(Document):
    complaintId = IntField(required=True)
    name = StringField(required=True)
    year = IntField()
    meta = {"collection": "complaints"}

def complaints_to_dict(complaint):
    d = complaint.to_mongo().to_dict()
    d['id'] = str(d.pop('_id'))
    return d

@app.route('/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.objects()
    return jsonify([complaints_to_dict(c) for c in complaints])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)