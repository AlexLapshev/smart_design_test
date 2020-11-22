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

var products = [
    {
        _id: 1,
        name: 'Xiaomi Note 6',
        description: 'Xiaomi Note 6 Description',
        parameters: {
            "color": "black",
            "brand": "Xiaomi",
            "operating_system": "Android",
            "screen_size": 6,
            "ram_size": 4
        }
    },
    {
        _id: 2,
        name: 'Iphone 12',
        description: 'Iphone 12 Description',
        parameters: {
            "color": "blue",
            "brand": "Iphone",
            "operating_system": "ios",
            "screen_size": 5,
            "ram_size": 3
        }
    },
    {
        _id: 3,
        name: 'Samsung S9',
        description: 'Samsung S9 Description',
        parameters: {
            "color": "pink",
            "brand": "Samsung",
            "operating_system": "Android",
            "screen_size": 7,
            "ram_size": 2
        }
    },
]

db.products.insertMany(products)