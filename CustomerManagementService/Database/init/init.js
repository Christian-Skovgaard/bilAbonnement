// Switch to your database
db = db.getSiblingDB("customerDB");

// Create a collection
db.createCollection("customers");

// Insert sample documents
db.customers.insertMany([
  {
    "firstName": "Liam",
    "lastName": "Thompson",
    "age": 28,
    "driversLicense": "T4873921",
    "isNice": true,
    "customerId":"1",
    "_id": "6936e20cd28bec25e19dc29d"
  },
  {
    "firstName": "Sophia",
    "lastName": "Martinez",
    "age": 32,
    "driversLicense": "M9283745",
    "customerId":"2",
    "_id": "6936e20cd28bec25e19dc29e"
  },
  {
    "firstName": "Ethan",
    "lastName": "Walker",
    "age": 24,
    "driversLicense": "W5638294",
    "customerId":"3",
    "_id": "6936e20cd28bec25e19dc29f"
  },
    {
    "firstName": "Olivia",
    "lastName": "Anderson",
    "age": 30,
    "driversLicense": "A7532941",
    "customerId":"4",
    "_id": "6936e20cd28bec25e19dc2a0"
  },
  {
    "firstName": "Noah",
    "lastName": "Bennett",
    "age": 27,
    "driversLicense": "B9821437",
    "customerId":"5",
    "_id": "6936e20cd28bec25e19dc2a1"
  }
]);