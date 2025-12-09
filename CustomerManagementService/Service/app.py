from flask import Flask, jsonify, request
import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from bson import Regex

myclient = pymongo.MongoClient("mongodb://customer-management-db:27017")
mydb = myclient["customerDB"] 
mycol = mydb["customers"] # Choose collection

app = Flask(__name__)

@app.route('/customers', methods=['GET'])
def get_customers():
    cursor = mycol.find({})
    customers = list(cursor)

    for customer in customers:    
        customer['_id'] = str(customer['_id'])
    
    return jsonify(customers)


# Get queried customers
@app.route('/customers/query', methods=['GET']) # Skal kunne tage højde for, om pris er INDEN FOR monthlyMin og monthlyMax
def search_customers():
    queryParams = request.args # Dict of query parameters
    query = []

    for key, value in queryParams.items():
        if (value != "" and type(value) is str):
            query.append({key: Regex(value, "i")}) # # Lav en liste af objekter til query ud fra query params f.eks.: [{brand : "Toyota"}, {model : "GT86"}]
        else:
            query.append({key: value})

    if query:
        mongo_filter = {"$and": query} # Request parameters given.
    else:
        mongo_filter = {}  # No request parameters given / empty request parameters like: ?brand=&model=

    print(mongo_filter)

    cursor = mycol.find(mongo_filter) # Query and remove MongoDB _id (surpress _id)
    customers = list(cursor)

    for customer in customers:    
        customer['_id'] = str(customer['_id'])

    return jsonify(customers)


@app.put('/customers/<customerId>')
def updateSub (customerId):
    reqBody = request.get_json()
    if not reqBody:
        return jsonify("no body attached"), 400
    
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(customerId)
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400


    customer = mycol.find_one({"_id": obj_id})
    if not customer:
        return jsonify("subscription matching ID not found"), 400
    
    result = mycol.update_one({"_id": obj_id}, {"$set": reqBody})

    return jsonify({
        "message": "Update successful",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    })


@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    cursor = mycol.insert_one(data)
    data['_id'] = str(cursor.inserted_id)
    return jsonify(data), 201

@app.delete('/customers/<customerId>')
def deleteCustomer(customerId):

    result = mycol.delete_one({"_id": ObjectId(customerId)}) # delete_many bare lige, hvis der på mærkelig vis var flere biler med samme reg. nr.
    return jsonify({
        "msg": "top sussecc 🏋️"
    })




@app.route('/test', methods=['GET'])
def test():
    
    return jsonify("i am alive 🧟")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)


