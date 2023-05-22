from datetime import datetime
import unittest
from src.rideshare import *
from tests.Init_test_data import *

class TestChat(unittest.TestCase):

  def setUp(self):
    """sets up the tables"""
    create_tables()
    init_test_data()

  def test_db_connect(self):
    """tests connection"""
    conn, cur = db_connect()
    self.assertIsNotNone(conn, "connection not made")
    self.assertIsNotNone(cur, "cursor not created")
    db_disconnect(conn)

  def test_db_disconnect(self):
    """tests disconnection"""
    conn, cur = db_connect()
    cur.close()
    result = db_disconnect(conn)
    self.assertFalse(result, "disconnection succesful")

  def test_get_driver(self):
    """test gets the driver with the entered id"""
    result = get_driver(1)
    self.assertIsNotNone(result, "Drivers Retrieved")

  def test_get_rider(self):
    """test gets the rider with the entered id"""
    result = get_rider(1)
    self.assertIsNotNone(result, "Riders Retrieved")
  
  def test_past_rides_given_tom(self):
    """tests that the rides given by mike is not none, he gave two rides"""
    result = get_past_rides_given(2, "Tom Magliozzi")
    self.assertNotEqual;([], result, "Past Rides Given Retrieved")

  def test_past_rides_given_mike(self):
    """tests that the rides given by mike (a rider) is none"""
    result = get_past_rides_given(1, "Mike Easter")
    self.assertListEqual([], result, "Past Rides Given Retrieved")

  def test_past_rides_taken_mike(self):
    """tests if rides taken are saved"""
    result = get_past_rides_taken(1, "Mike Easter")
    self.assertIsNotNone(result, "Past Rides Taken Retrieved")

  def test_get_rating(self):
    """tests if rating can be retrieved"""
    result = get_rating(2, "driver")
    self.assertEqual((3.4,), result, "Rating Retrieved")

  def test_get_instructions(self):
    """tests if instructions can be retrieved"""
    result = get_instructions(1, "driver")
    self.assertEqual(('Dont drive like my brother.',), result, "Rating Retrieved")

  def test_insert_data(self):
    """tests if data from the csv can be enetered, halted for other tests"""
    result = add_data("rideshare.csv")
    self.assertIsNotNone( result, "Data Not entered")
  
  def test_create_account(self):
    """tests that account is added to data"""
    driver = create_account("driver", "Hoke Colburn", "2/2/2023")
    rider = create_account("rider", "Ms. Daisy", "2/2/2023")
    self.assertIsNotNone(driver,  "No account created")
    self.assertIsNotNone(rider,  "No account created")

  def test_update_rating(self):
    """tests that rating can be updated"""
    pre_update_driver = get_rider(1)
    update_rating("driver", 1, 5.0)
    post_update_driver = get_rider(1)
    self.assertLessEqual(pre_update_driver, post_update_driver, "rating not updated")

  def test_cancel_ride(self):
    """tests that a ride can be cancled"""
    pre, post = cancel_ride(2, "Ayden Boyko")
    self.assertNotEqual(pre, post, "ride not canceled")

  def test_get_new_rider(self):
    """tests that a driver is able to see all riders with the same zipcode"""
    result = get_new_rider("30301")
    self.assertNotEqual([], result, "riders not found")

  def test_get_new_rider(self):
    """tests that a rider is able to see all drivers with the same zipcode"""
    result = get_new_drivers("30301")
    self.assertNotEqual([], result, "riders not found")

  def test_deactivate_account(self):
    """tests that account can be deactivated"""
    create_account("rider", "Ms. Daisy", "2/2/2023")
    pre_update_driver = get_rider(3)
    deactivate_account("rider", 3)
    post_update_driver = get_rider(3)
    #Compares the result of a query getting the first account that isnt deactivated
    self.assertNotEqual(pre_update_driver, post_update_driver, "No account deactivated")

  def test_change_ride_status(self):
    """tests that wants_ride can be set to false"""
    create_account("rider", "Ms. Daisy", "2/2/2023")
    pre = get_rider(3)
    change_ride_status(3)
    post = get_rider(3)
    self.assertNotEqual(pre, post, "wants_ride not changed")

  def test_new_ride(self):
    """tests that new rides can be added to current_rides"""
    create_account("rider", "Ms. Daisy", "2/2/2023")
    create_account("driver", "Hoke Colburn", "2/2/2023")
    pre = get_current_ride(3)
    new_ride(3, "Hoke Colburn", 3, "Ms. Daisy")
    post = get_current_ride(3)
    self.assertNotEqual(pre, post, "new ride not added")

  def test_update_instructions(self):
    """tests that special instructions can be updated"""
    pre_update_driver = get_driver(1)
    update_instructions("driver", 1, "drive like its you last day on earth")
    post_update_driver = get_driver(1)
    self.assertNotEqual(pre_update_driver , post_update_driver, "updates not made")

  def test_finish_ride(self):
    """test that completes the ongoing ride"""
    create_account("rider", "Ms. Daisy", "3/12/1967")
    create_account("driver", "Hoke Colburn", "5/24/1960")
    new_ride(3, "Hoke Colburn", 3, "Ms. Daisy")
    pre = get_past_rides_taken(3, "Ms.Daisy")
    rider_finish_ride(3, 5.0, "He drove well", datetime(1989, 12, 13))
    #The reason driver also ends the ride is to leave a review
    driver_finish_ride(3, 3, 5.0, "she was nice", datetime(1989, 12, 13))
    post = get_past_rides_taken(3, "Ms. Daisy")
    self.assertNotEqual(pre, post, "current ride not completed")

  def test_reactivate_account(self):
    """tests that accounts can be reactivated"""
    #deactivates account so it can be reactivated
    create_account("rider", "Ms. Daisy", "2/2/2023")
    deactivate_account("rider", 3)
    
    pre_update_rider = get_rider(3)
    reactivate_account("rider", 3)
    post_update_rider = get_rider(3)
    #Compares the result of a query getting the first account that isnt deactivated
    self.assertNotEqual(pre_update_rider, post_update_rider, "No account reactivated")

  def test_get_next_ride(self):
    """tests that rider can update their zipcode and wants_ride status to yes"""
    create_account("rider", "Ms. Daisy", "2/2/2023")
    pre_update_driver = get_rider(3)
    get_next_ride(3, '30301')
    post_update_driver = get_rider(3)
    #Compares the result of a query getting the first account that isnt deactivated
    self.assertNotEqual(pre_update_driver, post_update_driver, "No account deactivated")

  def test_respond(self):
    """tests that riders or drivers can respond"""
    pre = get_past_rides_given(2, "Tom Magliozzi")
    respond(2, "driver", "He was great!")
    post = get_past_rides_given(2, "Tom Magliozzi")
    #if the result are equal then no response was left
    self.assertNotEqual(pre, post, "No response added to past_rides")

  def test_get_reviews(self):
    """returns all the reviews associated with a person, inlcuding responses from drivers or passengers"""
    result = get_reviews(2, "driver")
    self.assertNotEqual([], result, "reviews not returned")

  def test_get_charge(self):
    """returns all bills associated with a id and name"""
    result, tab = get_bills(1, 'Mike Easter')
    self.assertIsNotNone(result, "bills not retrieved")
    self.assertEqual(9.5, tab, "total money not retrieved")

  def test_charge(self):
    """creates a bill for a rider"""  
    pre = get_bills(1, 'Mike Easter')
    charge(1, 'Mike Easter', 5.0, datetime(2007, 11, 24))
    post = get_bills(1, 'Mike Easter')
    self.assertNotEqual(pre, post, "bill not added")

  def test_change_carpool(self):
    """tests that the driver's carpool status changes"""
    pre = get_driver(1)
    change_carpool(1, '94131')
    post = get_driver(1)
    self.assertNotEqual(pre, post, "carpool status not changed")

  def test_find_drivers_carpool(self):
    """tests that carpool drivers within zipcode can be found"""
    change_carpool(1, '94131')
    result = find_drivers_carpool('94131')
    self.assertListEqual(['("Ray Magliozzi",0)'], result, "no drivers found")

  def test_join_carpool(self):
    """tests if carpool can be made, and when it reaches capacity, its marked as full, if none can be found, returns none"""
    #compares the amount of drivers before a carpool is full and after, the number should be less

    create_account("rider", "Alex Myan", "7/16/1995")
    create_account("rider", "Sarah Mitchell", "5/21/1989")
    create_account("rider", "Jared Fletcher", "2/2/2023")
    create_account("rider", "Max Gardner", "1/17/2001")
    create_account("driver", "David Genma", "11/26/1987")
    
    change_carpool(3, '94131')

    join_carpool(3, 'David Genma', 1, 'Alex Myan', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 2, 'Sarah Mitchell', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 3, 'jared Fletcher', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 4, 'Max Gardner', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    
    post = find_drivers_carpool('94131')

    self.assertEqual(None, post, "carpool not marked as full")

  def test_end_carpool(self):
    """tests that a passenger can be removed from the carpool once they are done, also bills them accordingly"""
    create_account("rider", "Alex Myan", "7/16/1995")
    create_account("rider", "Sarah Mitchell", "5/21/1989")
    create_account("rider", "Jared Fletcher", "2/2/2023")
    create_account("rider", "Max Gardner", "1/17/2001")
    create_account("driver", "David Genma", "11/26/1987")
    
    change_carpool(3, '94131')

    join_carpool(3, 'David Genma', 1, 'Alex Myan', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 2, 'Sarah Mitchell', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 3, 'jared Fletcher', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    join_carpool(3, 'David Genma', 4, 'Max Gardner', 'Get me there', '0,0', datetime(2023, 1, 1), '94131')
    
    pre = find_drivers_carpool('94131')

    rider_finish_ride(1, 4.5, "I liked how fast they drove", datetime(2023, 1, 1), True)
    respond(3, "driver", "Thank you for being a good passenger")

    post = find_drivers_carpool('94131')

    self.assertNotEqual(pre, post, "carpool not ended")

  def test_fare_times(self):
    """tests that all fares associated with a time can be retrieved"""
    create_account("rider", "Elias Banma", datetime(2000, 6, 19))
    create_account("driver", "Damian Guten", datetime(1987, 8, 22))

    #rider updates zipcode and staus of wants ride
    update_zipcode("rider", 3, '94131')
    change_ride_status(3)

    #driver searches for riders within zipcode
    riders = get_new_rider('94131')

    #rider searches for drivers within zipcode
    drivers = get_new_drivers('94131')

    #new ride created
    new_ride(drivers[0], drivers[1], riders[0], riders[1], "no instructions", riders[2])
    

    rider_finish_ride(riders[0], 5.0, "I liked their car", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)
    driver_finish_ride(drivers[0], riders[0], 4.7, "Pleasant passenger, had muddy shoes though.", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)

    result = fare_times(datetime(2023, 1, 1, 4))

    self.assertNotEqual([], result, "fares not retrieved")

  def test_full_ride_info(self):
    """tests that all info associated with a date can be retrieved"""
    create_account("rider", "Elias Banma", datetime(2000, 6, 19))
    create_account("driver", "Damian Guten", datetime(1987, 8, 22))
    update_zipcode("rider", 3, '94131')
    change_ride_status(3)
    new_ride(3, "Damian Guten", 3, "Elias Banma", "no instructions", '0,0')
    

    rider_finish_ride(3, 5.0, "I liked their car", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)
    driver_finish_ride(3, 3, 4.7, "Pleasant passenger, had muddy shoes though.", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)
    

    new_ride(3, "Damian Guten", 1, "Mike Easter", "no instructions", '0,0')
    rider_finish_ride(1, 4.0, "I liked their car", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)
    driver_finish_ride(3, 3, 4.7, "Pleasant passenger, had muddy shoes though.", datetime(2023, 1, 1, 4, 0, 0), False, 5.0)

    result = full_ride_info(datetime(2023, 1, 1, 4, 0, 0))

    self.assertIsNotNone(result, "ride info could not be retrieved")
