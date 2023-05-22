
In the future, if we were to add the ability to have surge pricing to your system, what would need to change? For example, maybe we want to surge the prices when there’s a lot of demand in one area at one time.
-implement a surge_price method that looks throught the list of riders looking for a ride, it then adjusts the pricing based on how many riders there are for that zipcode, all rides within that zipcode are affected

What tables need changing and/or adding?
-I would add a zipcode table that keeps track of how many riders are in a certain zipcode. For example, i take a ride at 4pm in the zipcode 94131, the bill could then be calculated by adding the cost of the ride at 4pm multiplied by the amount of riders in my zip every 50 users lets say the bill is doubled.

What API methods would you provide?
-get_zipcode_riders would retrieve the number of riders within a certain zipcode
-add_to_zipcode would increment the number of riders associated with the zipcode when said rider changes their zipcode

How might existing API methods change?
-bill method would use get_zipcode_riders method to incorporate surge based pricing.


In the future, if we were to add the ability to have future scheduling to your system, what would need to change? For example, a user would want to book a fare several days in advance.
-a new table called booked rides could be made to store rides that have been booked, once the date rolls around, they are added to current rides, and continue through the ride process

What tables need changing and/or adding?
-Because I already have a past_rides and curren_rides table, I would add a future_rides table.

What API methods would you provide?
-schedule_ride would schedule a ride for the rider based on their zipcode and time.

How might existing API methods change?
-not many methods would change. The user will still be billed for their ride once it is completed.
