db.Rides.aggregate([
  {
    $facet: {
      max_fare: [
        { $group: { _id: null, max_fare: { $max: "$fare" } } },
        { $project: { _id: 0, max_fare: "$max_fare" } }
      ],
      min_fare: [
        { $group: { _id: null, min_fare: { $min: "$fare" } } },
        { $project: { _id: 0, min_fare: "$min_fare" } }
      ]
    }
  },
  {
    $project: {
      rides: {
        $filter: {
          input: "$$ROOT",
          as: "ride",
          cond: {
            $or: [
              { $eq: ["$$ride.fare", { $arrayElemAt: ["$max_fare.max_fare", 0] }] },
              { $eq: ["$$ride.fare", { $arrayElemAt: ["$min_fare.min_fare", 0] }] }
            ]
          }
        }
      }
    }
  },
  { $unwind: "$rides" },
  { $replaceRoot: { newRoot: "$rides" } }
])
------------------------------------------------------------------------------------------------

db.Rides.aggregate([
  {
    $group: {
      _id: "$driver_id",
      average_fare: { $avg: "$fare" },
      average_distance: { $avg: "$distance" }
    }
  },
  {
    $project: {
      driver_id: "$_id",
      average_fare: 1,
      average_distance: 1,
      _id: 0
    }
  }
])
--------------------------------------------------------------------------------------------------------

db.Rides.aggregate([
  {
    $group: {
      _id: "$driver_id",
      ride_count: { $sum: 1 }
    }
  },
  {
    $match: {
      ride_count: { $gt: 5 }
    }
  },
  {
    $project: {
      driver_id: "$_id",
      ride_count: 1,
      _id: 0
    }
  }
])
-----------------------------------------------------------------------------------------------

db.Drivers.aggregate([
  {
    $lookup: {
      from: "Rides",
      localField: "driver_id",
      foreignField: "driver_id",
      as: "rides"
    }
  },
  {
    $unwind: "$rides"
  },
  {
    $group: {
      _id: "$driver_id",
      name: { $first: "$name" },
      max_fare: { $max: "$rides.fare" }
    }
  },
  {
    $match: {
      max_fare: { $eq: { $max: "$max_fare" } }
    }
  },
  {
    $project: {
      _id: 0,
      name: 1
    }
  }
])
-----------------------------------------------------------------------------

db.Rides.aggregate([
  {
    $group: {
      _id: "$driver_id",
      total_earnings: { $sum: "$fare" }
    }
  },
  {
    $sort: {
      total_earnings: -1
    }
  },
  {
    $limit: 3
  },
  {
    $project: {
      driver_id: "$_id",
      total_earnings: 1,
      _id: 0
    }
  }
])
-----------------------------------------------------------------------------------

db.Rides.find({
  ride_date: { $gte: new Date(new Date().setDate(new Date().getDate() - 7)) }
})
-------------------------------------------------------------------------------------
db.Rides.find({
  $or: [
    { end_location: null },
    { end_location: "" }
  ]
})
-----------------------------------------------------------------------------------------
db.Rides.aggregate([
  {
    $project: {
      id: 1,
      fare_per_mile: { $divide: ["$fare", "$distance"] }
    }
  },
  {
    $sort: {
      fare_per_mile: -1
    }
  }
])
---------------------------------------------------------------------------------------
db.Rides.aggregate([
  {
    $lookup: {
      from: "Drivers",
      localField: "driver_id",
      foreignField: "driver_id",
      as: "driver"
    }
  },
  {
    $unwind: "$driver"
  },
  {
    $lookup: {
      from: "Passengers",
      localField: "passenger_id",
      foreignField: "passenger_id",
      as: "passenger"
    }
  },
  {
    $unwind: "$passenger"
  },
  {
    $project: {
      _id: 0,
      id: "$id",
      driver_name: "$driver.name",
      passenger_name: "$passenger.name"
    }
  }
])
------------------------------------------------------------------------------------------------
db.Rides.insertOne({
  driver_id: 123,
  passenger_id: 456,
  ride_date: new Date(),
  fare: 20.00,
  start_location: "123 Main Street",
  end_location: "456 Elm Avenue",
  tip: 3.50
})