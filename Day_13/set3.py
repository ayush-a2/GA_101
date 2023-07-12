
db.createCollection("Rides", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["customer_id", "driver_id", "ride_date", "fare", "start_location", "end_location"],
         properties: {
            id: {
               bsonType: "int"
            },
            customer_id: {
               bsonType: "int"
            },
            driver_id: {
               bsonType: "int"
            },
            ride_date: {
               bsonType: "date"
            },
            fare: {
               bsonType: "decimal",
               minimum: 0,
               maximum: 999999.99
            },
            start_location: {
               bsonType: "string"
            },
            end_location: {
               bsonType: "string"
            }
         }
      }
   }
})
-----------------------------------------------------------------------------------

db.Rides.insertMany([
   {
      customer_id: 1,
      driver_id: 101,
      ride_date: new Date('2023-07-10'),
      fare: 15.50,
      start_location: '123 Main Street',
      end_location: '456 Elm Avenue'
   },
   {
      customer_id: 2,
      driver_id: 102,
      ride_date: new Date('2023-07-11'),
      fare: 20.75,
      start_location: '789 Oak Road',
      end_location: '321 Pine Lane'
   },
   {
      customer_id: 3,
      driver_id: 103,
      ride_date: new Date('2023-07-12'),
      fare: 18.25,
      start_location: '654 Cedar Court',
      end_location: '987 Maple Avenue'
   },
   {
      customer_id: 4,
      driver_id: 104,
      ride_date: new Date('2023-07-13'),
      fare: 12.80,
      start_location: '246 Oak Street',
      end_location: '135 Elm Drive'
   },
   {
      customer_id: 5,
      driver_id: 105,
      ride_date: new Date('2023-07-14'),
      fare: 9.95,
      start_location: '789 Pine Lane',
      end_location: '369 Maple Road'
   }
])
--------------------------------------------------------------------
db.Rides.find().sort({ fare: -1 })
---------------------------------------------------------------------
db.Rides.aggregate([
  {
    $group: {
      _id: null,
      total_distance: { $sum: "$distance" },
      total_fare: { $sum: "$fare" }
    }
  }
])
------------------------------------------------------------------------
db.Rides.aggregate([
  {
    $group: {
      _id: null,
      average_ride_time: { $avg: "$ride_time" }
    }
  }
])
--------------------------------------------------------------------
db.Rides.find({
  $or: [
    { start_location: { $regex: 'Downtown' } },
    { end_location: { $regex: 'Downtown' } }
  ]
})
------------------------------------------------------------------
db.Rides.countDocuments({ driver_id: <driver_id> })
-----------------------------------------------------------------
db.Rides.updateOne({ id: 4 }, { $set: { fare: <new_fare> } })
---------------------------------------------------------------------

db.Rides.aggregate([
  {
    $group: {
      _id: "$driver_id",
      total_fare: { $sum: "$fare" }
    }
  }
])
-----------------------------------------------------------------------------
db.Rides.deleteOne({ id: 2 })