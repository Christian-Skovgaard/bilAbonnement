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
    "isNice": true
  },
  {
    "firstName": "Sophia",
    "lastName": "Martinez",
    "age": 32,
    "driversLicense": "M9283745"
  },
  {
    "firstName": "Ethan",
    "lastName": "Walker",
    "age": 24,
    "driversLicense": "W5638294"
  },
    {
    "firstName": "Olivia",
    "lastName": "Anderson",
    "age": 30,
    "driversLicense": "A7532941"
  },
  {
    "firstName": "Noah",
    "lastName": "Bennett",
    "age": 27,
    "driversLicense": "B9821437"
  }
]);