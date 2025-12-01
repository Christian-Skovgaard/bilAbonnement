// Switch to your database (will be created automatically)
db = db.getSiblingDB("car-catalog-db");

// Create a collection
db.createCollection("cars");

// Insert sample documents (optional)
db.cars.insertMany([
  { make: "Toyota", model: "Corolla", year: 2020 },
  { make: "Honda", model: "Civic", year: 2021 }
]);





/*

// Optional: create a non-root user
db.createUser({
  user: "appuser",
  pwd: "apppassword",
  roles: [
    { role: "readWrite", db: "car-catalog" }
  ]
});

*/