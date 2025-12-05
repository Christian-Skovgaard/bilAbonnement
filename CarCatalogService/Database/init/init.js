// Switch to your database
// Switch to your database
db = db.getSiblingDB("car-catalog-db");

// Car JSON schema validation
db.createCollection("cars", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["regNr", "brand", "model", "modelYear", "propellant", "kmDriven", "monthlyPrice", "available"],
      additionalProperties: false,
      properties: {
        _id: {
          bsonType: "objectId"
        },
        regNr: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        brand: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        model: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        modelYear: {
          bsonType: "int",
          minimum: 1886, // first car invented
          maximum: 2100,
          description: "must be an integer year"
        },
        propellant: {
          bsonType: "string",
          enum: ["Benzin", "Diesel", "El", "Hybrid"],
          description: "must be one of the allowed fuel types"
        },
        kmDriven: {
          bsonType: "int",
          minimum: 0,
          description: "must be a non-negative integer"
        },
        monthlyPrice: {
          bsonType: "int",
          minimum: 0,
          description: "must be a non-negative integer"
        },
        available: {
          bsonType: "bool",
          description: "must be true or false"
        }
      }
    }
  },
  validationAction: "error" // reject invalid inserts/updates
});


// Insert sample documents
db.cars.insertMany([
  {
    regNr: "XD69420",
    brand: "Toyota",
    model: "GT86",
    modelYear: 2012,
    propellant: "Benzin",
    kmDriven: 250000,
    monthlyPrice: 8000,
    available: true
  },
  {
    regNr: "JD97731",
    brand: "Chevrolet",
    model: "Suburban",
    modelYear: 2006,
    propellant: "Benzin",
    kmDriven: 470000,
    monthlyPrice: 4100,
    available: true
  },
  {
    regNr: "BQ38126",
    brand: "Audi",
    model: "A6",
    modelYear: 2008,
    propellant: "Benzin",
    kmDriven: 360000,
    monthlyPrice: 6000,
    available: true
  },
  {
    regNr: "DO17851",
    brand: "BMW",
    model: "X1",
    modelYear: 2019,
    propellant: "Diesel",
    kmDriven: 120000,
    monthlyPrice: 9500,
    available: false
  },
  {
    regNr: "AD46784",
    brand: "Citroen",
    model: "Berlingo",
    modelYear: 2008,
    propellant: "Benzin",
    kmDriven: 80000,
    monthlyPrice: 3000,
    available: true
  },
  {
    regNr: "UG23317",
    brand: "Hyundai",
    model: "Kona",
    modelYear: 2022,
    propellant: "El",
    kmDriven: 28000,
    monthlyPrice: 6300,
    available: true
  },
  {
    regNr: "TP68117",
    brand: "Kia",
    model: "Niro",
    modelYear: 2019,
    propellant: "Hybrid",
    kmDriven: 96000,
    monthlyPrice: 5600,
    available: true
  }
]);