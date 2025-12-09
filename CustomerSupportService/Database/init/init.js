// Switch to your database
db = db.getSiblingDB("customer-service-db");

// Create a collection
db.createCollection("complaints");

// Insert sample documents
db.complaints.insertMany([
  { 
    regNr: "XD69420", 
    name: "Magnus", 
    date: "16/04/2023",
    complaint: "Har betalt for meget for den periode jeg har haft bilen.",
    completed: true
  },


  { 
    regNr: "XD69420", 
    name: "Magnus", 
    date: "16/04/2023", 
    complaint: "Har betalt for meget for den periode jeg har haft bilen.", 
    completed: true 
  },

  { 
    regNr: "AB11223", 
    name: "Sara Jensen", 
    date: "22/05/2023", 
    complaint: "Blev opkrævet for et serviceeftersyn som allerede var inkluderet i aftalen.", 
    completed: false 
  },

  { 
    regNr: "CT99887", 
    name: "Jonas Mortensen", 
    date: "02/07/2023", 
    complaint: "Bilen blev leveret for sent, og der blev stadig opkrævet fuld månedspris.", 
    completed: true 
  },

  { 
    regNr: "FG55661", 
    name: "Lene Kristoffersen", 
    date: "11/09/2023", 
    complaint: "Har fået en ekstraregning for kilometer, men måleren i bilen stemmer ikke overens.", 
    completed: false 
  },

  { 
    regNr: "ZX44321", 
    name: "Peter Holm", 
    date: "28/10/2023", 
    complaint: "Opsigelsesgebyret er højere end det, der står i kontrakten.", 
    completed: true 
  },

  { 
    regNr: "LK77889", 
    name: "Amalie Sørensen", 
    date: "03/01/2024", 
    complaint: "Har betalt for en ekstra måned, selvom bilen blev afleveret før periodens udløb.", 
    completed: false 
  }

]);