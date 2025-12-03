from flask import Flask, jsonify, request
from mongoengine import connect, Document, StringField, IntField


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


@app.route('/complaints', methods=['POST'])
def add_complaints():
    data = request.get_json(force=True)
    complaintId = data.get('complaintId')
    name = data.get('name')
    year = data.get('year')
    complaints = Complaint(complaintId=complaintId, name=name, year=year)
    complaints.save()
    return jsonify(complaints_to_dict(complaints)), 201


#get complaints by query parameters
@app.route('/complaints/query', methods=['GET'])
def search_complaints():
    complaintId = request.args.get('complaintId')
    name = request.args.get('name')
    year = request.args.get('year')

    filters = {}
    
    if complaintId:
        filters['complaintId'] = int(complaintId)  
    
    if name:
        filters['name__icontains'] = name

    if year:
        filters['year'] = int(year)

    complaints = Complaint.objects(**filters)

    return jsonify([complaints_to_dict(c) for c in complaints])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)