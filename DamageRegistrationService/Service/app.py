from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://damage-registrations-db:27017")
mydb = myclient["damage-registrations-db"] # Choose database "car-catalog-db"
mycol = mydb["registrations"] # Choose collection

app = Flask(__name__)

# Get all registrations
@app.route('/registrations', methods=['GET'])
def get_registrations():
    cursor = mycol.find({}, {"_id": 0}) # Query and remove MongoDB _id (surpress_id)
    registrations = list(cursor)
    return jsonify(registrations)

# Get queried registrations
@app.route('/registrations/query', methods=['GET']) # Skal kunne tage højde for, om pris er INDEN FOR monthlyMin og monthlyMax
def search_registrations():
    queryParams = request.args # Dict of query parameters
    query = []

    for key, value in queryParams.items():
        if value != "":
            query.append({key: value}) # Lav en liste af objekter til query ud fra query params f.eks.: [{brand : "Toyota"}, {model : "GT86"}]

    if query:
        mongo_filter = {"$and": query} # Request parameters given.
    else:
        mongo_filter = {}  # No request parameters given / empty request parameters like: ?brand=&model=

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    registrations = list(cursor)
    return jsonify(registrations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)


