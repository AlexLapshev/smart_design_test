db.createUser(
    {
        user: "smart_design_user",
        pwd: "123456",
        roles: [
            {
                role: "readWrite",
                db: "smart_design_mongo"
            }
        ]
    }
)

var parameters = {
  items: {
    bsonType: "object",
    required: ["color", "brand", "operating_system", "screen_size", "ram_size"],
    properties: {
      color: {
        bsonType: "string"
      },
      brand: {
        bsonType: "string"
      },
      operating_system: {
        bsonType: "string"
      },
      screen_size: {
        bsonType: "int"
      },
      ram_size: {
        bsonType: "int"
      }
    }
  }
}

db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "description", "parameters"],
      properties: {
        name: {
            bsonType: "string"
        },
        name: {
            description: "string"
        },
        parameters: parameters
      },
    }
  }
})
