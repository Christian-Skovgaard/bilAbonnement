// Switch to your database
db = db.getSiblingDB("subscriptionDB");

// Create a collection
db.createCollection("subscriptions");

// Insert sample documents
db.subscriptions.insertMany([
  {
    regNr: "XD 69 420",
    brand: "Toyota",
    model: "GT86",
    modelYear: 2012,
    propellant: "Benzin",
    kmDriven: 250000,
    monthlyPrice: 8000,
    available: true
  },
  {
    regNr: "JD 97 731",
    brand: "Chevrolet",
    model: "Suburban",
    modelYear: 2006,
    propellant: "Benzin",
    kmDriven: 470000,
    monthlyPrice: 4100,
    available: true
  },
  {
    regNr: "BQ 38 126",
    brand: "Audi",
    model: "A6",
    modelYear: 2008,
    propellant: "Benzin",
    kmDriven: 360000,
    monthlyPrice: 6000,
    available: true
  },
  {
    regNr: "DO 17 851",
    brand: "BMW",
    model: "X1",
    modelYear: 2019,
    propellant: "Diesel",
    kmDriven: 120000,
    monthlyPrice: 9500,
    available: false
  },
  {
    regNr: "AD 46 784",
    brand: "Citroen",
    model: "Berlingo",
    modelYear: 2008,
    propellant: "Benzin",
    kmDriven: 80000,
    monthlyPrice: 3000,
    available: true
  },
  {
    regNr: "UG 23 317",
    brand: "Hyundai",
    model: "Kona",
    modelYear: 2022,
    propellant: "El",
    kmDriven: 28000,
    monthlyPrice: 6300,
    available: true
  },
  {
    regNr: "TP 68 117",
    brand: "Kia",
    model: "Niro",
    modelYear: 2019,
    propellant: "Hybrid",
    kmDriven: 96000,
    monthlyPrice: 5600,
    available: true
  }
]);