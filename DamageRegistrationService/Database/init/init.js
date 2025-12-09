// Switch to your database
db = db.getSiblingDB("damage-registration-db");

// Create a collection
db.createCollection("cases", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["regNr", "desc", "date", "status", "reparationCost"],
      additionalProperties: false,
      properties: {
        _id: {
          bsonType: "objectId"
        },
        regNr: {
          bsonType: "string",
          description: "must be a string"
        },
        desc: {
          bsonType: "string",
          description: "must be a string"
        },
        date: {
          bsonType: "string", // Kunne være 'date', men ved ikke om det bliver for besværeligt.
          description: "must be a string"
        },
        status: {
          bsonType: "string",
          enum: ["Repareret", "Under reparation", "Ikke repareret"],
          description: "must be: 'Repareret', 'Under reparation', or 'Ikke repareret'"
        },
        reparationCost: {
          bsonType: "int",
          minimum: 0,
          description: "must be an integer"
        }
      }
    }
  },
  validationAction: "error" // reject invalid inserts/updates
});

// Insert sample documents
db.cases.insertMany([
  {
    "regNr": "XD69420",
    "desc": "Dyb ridse, ca. 40 cm lang på højre bagskærm, som strækker sig fra hjulkassen og op til tankdækslet. Kofangeren er revnet, ca. 10 cm lang flænge, og trykket en smule ind i højre side. Højre baglygte er intakt, men ydre plastkant er let skrammet.",
    "date": "14/07/2020",
    "status": "Repareret",
    "reparationCost": 17500
  },
  {
    "regNr": "XD69420",
    "desc": "Buler og skrammer på venstre fordør efter uagtsomt åbnet dør fra en parkeret bil. Låsemekanismen fungerer stadig, men døren skal udrettes og lakeres.",
    "date": "03/11/2021",
    "status": "Repareret",
    "reparationCost": 8950
  },
  {
    "regNr": "XD69420",
    "desc": "Stenslag på forruden i førerens synsfelt. Stenslaget er større end en 2-krone og kan ikke repareres; kræver udskiftning af hele forruden.",
    "date": "25/02/2022",
    "status": "Under reparation",
    "reparationCost": 3200
  },
  {
    "regNr": "JD97731",
    "desc": "Påkørsel bagfra ved lav hastighed. Bagkofanger stærkt deformeret og skal udskiftes. Bagklap sidder skævt og har lette buler, kræver justering og pladearbejde.",
    "date": "01/09/2023",
    "status": "Repareret",
    "reparationCost": 22400
  },
  {
    "regNr": "JD97731",
    "desc": "Små, overfladiske ridser (vaskeridser) over hele kølerhjelmen. Egenbetaling er højere end reparationsomkostningen.",
    "date": "10/05/2024",
    "status": "Ikke repareret",
    "reparationCost": 1500
  },
  {
    "regNr": "BQ38126",
    "desc": "Bakkameraet er holdt op med at fungere efter kraftig regn. Diagnosticering viser en defekt ledningsforbindelse, der kræver udskiftning af kameraenheden.",
    "date": "19/12/2020",
    "status": "Under reparation",
    "reparationCost": 6100
  },
  {
    "regNr": "BQ38126",
    "desc": "Skade på højre forskærm og forreste kofangerhjørne efter sammenstød med en betonpullert ved lav hastighed. Kræver udretning af forskærm og lakering af både forskærm og kofanger.",
    "date": "08/04/2021",
    "status": "Repareret",
    "reparationCost": 11500
  },
  {
    "regNr": "DO17851",
    "desc": "Bilens emblem på kølerhjelmen er ridset og falmet. Erstatning anses for kosmetisk og dækkes ikke af forsikringen.",
    "date": "02/07/2021",
    "status": "Ikke repareret",
    "reparationCost": 900
  },
  {
    "regNr": "DO17851",
    "desc": "Haglskade over hele bilens tag og kølerhjelm. Talrige små buler (ca. 40-50 stk.) kræver PDR (Paintless Dent Repair) eller fuld udskiftning og lakering af taget.",
    "date": "20/01/2022",
    "status": "Under reparation",
    "reparationCost": 35800
  },
  {
    "regNr": "AD46784",
    "desc": "Skade på venstre sidespejl (knust spejlglas og beskadiget kappe) efter et møde med en forbikørende lastbil. Sidespejlet skal udskiftes komplet.",
    "date": "17/06/2022",
    "status": "Repareret",
    "reparationCost": 14200
  },
  {
    "regNr": "AD46784",
    "desc": "Fejl på ABS-sensor i højre forhjul. Kræver udskiftning af sensoren og nulstilling af fejlmeldinger i bilens computer.",
    "date": "12/03/2023",
    "status": "Repareret",
    "reparationCost": 7900
  },
  {
    "regNr": "UG23317",
    "desc": "Tyveriforsøg: Låsen på venstre fordør er brudt op og ødelagt. Døren kan ikke låses/oplåses. Kræver udskiftning af låsemekanisme og reparation/lakering af dørpanelet omkring låsen.",
    "date": "29/08/2023",
    "status": "Ikke repareret",
    "reparationCost": 19500
  },
  {
    "regNr": "UG23317",
    "desc": "Stenslag repareret på forruden i passagersiden, uden for førerens synsfelt. Kun harpiksreparation.",
    "date": "05/11/2023",
    "status": "Repareret",
    "reparationCost": 4100
  },
  {
    "regNr": "TP68117",
    "desc": "Påkørsel af rådyr: Skader på frontgitter, køler, og motorhjelmen er bøjet. Kræver udskiftning af køler, gitter og pladearbejde på motorhjelmen.",
    "date": "07/04/2024",
    "status": "Under reparation",
    "reparationCost": 28900
  },
  {
    "regNr": "TP68117",
    "desc": "En bule i venstre side af bilens tag efter et faldet æble. Skaden er minimal og dækkes ikke, da beløbet er under selvrisikoen.",
    "date": "01/08/2024",
    "status": "Ikke repareret",
    "reparationCost": 1100
  }
]);