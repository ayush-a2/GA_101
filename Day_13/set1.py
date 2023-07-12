db.createCollection("Customers", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["name", "email", "address", "phone_number"],
         properties: {
            id: {
               bsonType: "int"
            },
            name: {
               bsonType: "string"
            },
            email: {
               bsonType: "string"
            },
            address: {
               bsonType: "string"
            },
            phone_number: {
               bsonType: "string"
            }
         }
      }
   }
})




---------------------------------------------------------------------------------------------

db.Customers.insertMany([
   {
      name: 'John Doe',
      email: 'johndoe@example.com',
      address: '123 Main Street',
      phone_number: '555-1234'
   },
   {
      name: 'Jane Smith',
      email: 'janesmith@example.com',
      address: '456 Elm Avenue',
      phone_number: '555-5678'
   },
   {
      name: 'Michael Johnson',
      email: 'michaeljohnson@example.com',
      address: '789 Oak Road',
      phone_number: '555-9012'
   },
   {
      name: 'Emily Davis',
      email: 'emilydavis@example.com',
      address: '321 Pine Lane',
      phone_number: '555-3456'
   },
   {
      name: 'David Wilson',
      email: 'davidwilson@example.com',
      address: '654 Cedar Court',
      phone_number: '555-7890'
   }
])

-------------------------------------------------------------------------------------------------
db.Customers.find({})
-------------------------------------------------------------------------------------------------

db.Customers.find({}, { name: 1, email: 1 })
------------------------------------------------------------------------------------------------

db.Customers.find({ id: 3 })

---------------------------------------------------------------------------------------------------

db.Customers.find({ name: { $regex: '^A' } })

----------------------------------------------------------------------------------------------------

db.Customers.find().sort({ name: -1 })
--------------------------------------------------------------------------------------------------

db.Customers.updateOne({ id: 4 }, { $set: { address: 'New Address' } })
-------------------------------------------------------------------------------------------------

db.Customers.deleteOne({ id: 2 })
------------------------------------------------------------------------------------------------

db.Customers.countDocuments({})
-----------------------------------------------------------------------------------------------
db.Customers.find().sort({ id: 1 }).skip(2)
----------------------------------------------------------------------------------------------------

SELECT * FROM Customers WHERE id > 2 AND name LIKE 'B%';
-------------------------------------------------------------------------------------------------

db.Customers.find({ $or: [ { id: { $lt: 3 } }, { name: { $regex: 's' } } ] })
----------------------------------------------------------------------------------------------

db.Customers.find({ $or: [ { phone_number: null }, { phone_number: '' } ] })
