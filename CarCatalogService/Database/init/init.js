// Switch to your database
db = db.getSiblingDB("car-catalog-db");

// Create a collection
db.createCollection("cars");

// Insert sample documents
db.cars.insertMany([
  { make: "Toyota", model: "Corolla", year: 2020, stelNR: "1HGCM82633A004352" },
  { make: "Honda", model: "Civic", year: 2021, stelNR: "2HGFB2F50CH512345" },
]);