from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://subscription-management-db:27017")
mydb = myclient["subscription-db"] # Choose database "car-catalog-db"
mycol = mydb["subscription"] # Choose collection

app = Flask(__name__)

@app.post('/createSubscription')
def createSubscription():
    None




@app.route('/test', methods=['GET'])
def test():
    return jsonify("i am alive")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)