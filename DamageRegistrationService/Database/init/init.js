// Switch to your database
db = db.getSiblingDB("damage-registration-db");

// Create a collection
db.createCollection("cases");

// Insert sample documents
db.cases.insertMany([
  {
    regNr: "XD69420",
    car: "Toyota",
    model: "GT86",
    modelYear: 2014,
    description: "crashed the car",
    date: "2025-01-12"
  },
  {
    regNr: "XD69420",
    car: "audi",
    model: "rs6",
    modelYear: 2016,
    description: "Hit a pole",
    date: "2022-02-10"
  }
]);