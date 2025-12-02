// Switch to your database
db = db.getSiblingDB("car-catalog-db");

// Create a collection
db.createCollection("cars");

// Insert sample documents
db.cars.insertMany([
  { make: "Toyota", model: "Corolla", year: 2020 },
  { make: "Honda", model: "Civic", year: 2021 }
]);