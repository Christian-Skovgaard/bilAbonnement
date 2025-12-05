// Switch to your database
db = db.getSiblingDB("damage-registrations-db");

// Create a collection
db.createCollection("damageCases");

// Insert sample documents
db.damageCases.insertMany([
  {
    regNr: "XD69420",
    car: "Toyota",
    model: "GT86",
    modelYear: 20014,
    description: "crashed the car",
    date: "2025-01-12"
  },
  {
    regNr: "XD69420",
    car: "audi",
    model: "rs6",
    modelYear: 20016,
    description: "Hit a pole",
    date: "2022-02-10"
  }
]);