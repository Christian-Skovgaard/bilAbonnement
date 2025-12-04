import pymongo
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

myclient = pymongo.MongoClient("mongodb://subscription-management-db:27017")
mydb = myclient["subscription-db"] # Choose database "car-catalog-db"
mycol = mydb["subscription"] # Choose collection

def insertSubscription (subObj):
    result = mycol.insert_one(subObj)
    print(f"Subscription inserted with _id: {result.inserted_id}")
    return {id: result.inserted_id}
   
