from flask import Flask, request, jsonify
import pymongo

myclient = pymongo.MongoClient("http://car-catalog-db:27017")
mydb = myclient["catalog"]
mycol = mydb["cars"]

x = mycol.find_one()

print(x)

app = Flask(__name__)

@app.route('/cars', methods=['GET'])
def getCars():
        return jsonify("Hi :3"), 200

app.run(host='0.0.0.0', port=5000)