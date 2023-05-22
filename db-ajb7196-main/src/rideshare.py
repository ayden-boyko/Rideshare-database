import itertools
from src.swen344_db_utils import connect, exec_sql_file
import csv
from datetime import datetime
from math import fsum

def create_tables():
    """drops, and then creates the sql and adds data to the sql tables"""
    try:
        exec_sql_file("init_test_schema.sql")
    except FileNotFoundError:
        print("sql files not found")

def db_connect():
    """connects to the database"""
    conn = connect()
    cur = conn.cursor()
    return conn, cur   

def db_disconnect(conn):
    """disconnects from database"""
    try:
        conn.commit()
        conn.close()
    except ConnectionError:
        print("could not disconnect")
        return False

def add_data(file):
    """adds data from a csv file into driver or rider tables"""
    conn, cur = db_connect()
    try:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                if row[1] == 'rider':
                    statement = """INSERT INTO rider (name, birthday) VALUES (%s, %s)"""
                    cur.execute(statement, [row[0], row[2]])
                elif row[1] == 'driver':
                    statement = """INSERT INTO driver (name, birthday) VALUES (%s, %s)"""
                    cur.execute(statement, [row[0], row[2]])
        db_disconnect(conn)
        return 0
    except FileNotFoundError:
        print("csv file not found")
        db_disconnect(conn)
        return None

def get_driver(id):
    """returns driver based on their id"""
    conn, cur = db_connect()
    
    drivers = """SELECT * FROM driver WHERE driver_id = %s"""

    cur.execute(drivers, (id,))
    result = cur.fetchone()
    db_disconnect(conn)
    return result

def get_rider(id):
    """returns rider based on their id"""
    conn, cur = db_connect()

    riders = """SELECT * FROM rider WHERE rider_id = %s"""

    cur.execute(riders, (id,))
    result = cur.fetchone()
    db_disconnect(conn)
    return result
    
def get_past_rides_taken(id, name):
    """returns past rides taken"""
    conn, cur = db_connect()

    rides = """SELECT * FROM past_rides WHERE r_id = %s AND rider_name = %s"""

    cur.execute(rides, [id, name])
    result = cur.fetchall()
    db_disconnect(conn)
    return result

def get_past_rides_given(id, name):
    conn, cur = db_connect()

    rides = """SELECT * FROM past_rides WHERE d_id = %s AND driver_name = %s"""

    cur.execute(rides, [id, name]) 
    result = cur.fetchall()
    db_disconnect(conn)
    return result

def get_rating(id, role):
    """returns rating"""
    conn, cur = db_connect()
    if role == "driver":
        rating = """SELECT rating FROM driver WHERE driver_id = %s"""
    else:
        rating = """SELECT rating FROM rider WHERE rider_id = %s"""

    cur.execute(rating, [id])
    result = cur.fetchone()
    db_disconnect(conn)
    return result

def get_instructions(id, role):
    """returns special instructions"""
    conn, cur = db_connect()
    if role == "driver":
        rating = """SELECT special_instructions FROM driver WHERE driver_id = %s"""
    else:
        rating = """SELECT special_instructions FROM rider WHERE rider_id = %s"""

    cur.execute(rating, [id])
    result = cur.fetchone()
    db_disconnect(conn)
    return result

def create_account(role, name, date):
    """creates an account"""
    conn, cur = db_connect()
    pre = cur.rowcount
    if role == "driver":
        statement = """INSERT INTO driver (name, birthday) Values (%s, %s) RETURNING driver_id"""
    else:
        statement = """INSERT INTO rider (name, birthday) Values (%s, %s) RETURNING rider_id"""
    cur.execute(statement, [name, date])
    result = cur.fetchone()
    db_disconnect(conn)
    return result

def deactivate_account(role, id):
    """deactivates an account"""
    conn, cur = db_connect()
    if role == "driver":

        statement = """UPDATE driver SET is_active = False WHERE driver_id = %s"""
        cur.execute(statement, [id])
    else:

        statement = """UPDATE rider SET is_active = False WHERE rider_id = %s"""
        cur.execute(statement, [id])

    db_disconnect(conn)

def change_ride_status(id):
    """changes wants ride"""
    conn, cur = db_connect()

    statement = """SELECT wants_ride FROM rider WHERE rider_id = %s"""
    cur.execute(statement, [id])
    wants_ride = cur.fetchone()
    
    statement = """UPDATE rider SET wants_ride = %s WHERE rider_id = %s"""
    cur.execute(statement, [not wants_ride, id])

    db_disconnect(conn)

def update_instructions(role, id, instructions):
    """updates the special instructions of the accounts"""
    conn, cur = db_connect()

    if role == "driver":
        statement = """UPDATE driver SET special_instructions = %s WHERE driver_id = %s"""
        cur.execute(statement, [instructions, id])
    
    elif role == "rider":
        statement = """UPDATE rider SET special_instructions = %s WHERE rider_id = %s"""
        cur.execute(statement, [instructions, id])

    db_disconnect(conn)

def change_ride_status(id):
    """changes wants ride"""
    conn, cur = db_connect()

    statement = """SELECT wants_ride FROM rider WHERE rider_id = %s"""
    cur.execute(statement, [id])
    wants_ride = cur.fetchone()
    
    statement = """UPDATE rider SET wants_ride = %s WHERE rider_id = %s"""
    cur.execute(statement, [not wants_ride[0], id])

    db_disconnect(conn)

def update_zipcode(role, id, zipcode):
    """updates the special instructions of the accounts"""
    conn, cur = db_connect()

    if role == "driver":
        statement = """SELECT zipcode FROM driver WHERE driver_id = %s"""
        cur.execute(statement, [id])
        pre = cur.fetchone()
    
        statement = """UPDATE driver SET zipcode = %s WHERE driver_id = %s"""
        cur.execute(statement, [zipcode, id])

        statement = """SELECT zipcode FROM driver WHERE driver_id = %s"""
        cur.execute(statement, [id])
        post = cur.fetchone()
    
    elif role == "rider":
        statement = """SELECT zipcode FROM rider WHERE rider_id = %s"""
        cur.execute(statement, [id])
        pre = cur.fetchone()

        statement = """UPDATE rider SET zipcode = %s WHERE rider_id = %s"""
        cur.execute(statement, [zipcode, id])

        statement = """SELECT zipcode FROM rider WHERE rider_id = %s"""
        cur.execute(statement, [id])
        post = cur.fetchone()

    db_disconnect(conn)
    return pre, post

def reactivate_account(role, id):
    """reactivates an account"""
    conn, cur = db_connect()
    if role == "driver":

        statement = """UPDATE driver SET is_active = %s WHERE driver_id = %s"""
        cur.execute(statement, [True, id])
    else:

        statement = """UPDATE rider SET is_active = %s WHERE rider_id = %s"""
        cur.execute(statement, [True, id])

    db_disconnect(conn)

def get_next_ride( id, zipcode):
    """changes wants ride"""
    conn, cur = db_connect()

    statement = """UPDATE rider SET wants_ride = True, zipcode = %s WHERE rider_id = %s"""
    cur.execute(statement, [ zipcode, id])

    db_disconnect(conn)

def update_rating(role, id, rating):
    """updates the average rating of the accounts"""
    conn, cur = db_connect()

    if role == "driver":
        statement = """SELECT rating FROM driver WHERE driver_id = %s"""
        cur.execute(statement, [id])
        pre = cur.fetchall()
        
        for i in range(len(pre)):
            rating += i
        
        rating = rating / len(pre)
    
        statement = """UPDATE driver SET rating = %s WHERE driver_id = %s"""
        cur.execute(statement, [rating, id])
    
    elif role == "rider":
        statement = """SELECT rating FROM rider WHERE rider_id = %s"""
        cur.execute(statement, [id])
        pre = cur.fetchall()
        
        for i in range(len(pre)):
            rating += i
        
        rating = rating / len(pre)
    
        statement = """UPDATE rider SET rating = %s WHERE rider_id = %s"""
        cur.execute(statement, [rating, id])


    db_disconnect(conn)

def new_ride(d_id, d_name, r_id, r_name, special_instructions = "No special instructions", start = '0,0'):
    """Adds a new ride to current rides"""
    conn, cur = db_connect()

    statement = """INSERT INTO current_rides (driver_id, d_name, rider_id, r_name, s_instructions, start) VALUES (%s, %s, %s, %s, %s, %s)"""
    cur.execute(statement, [d_id, d_name, r_id, r_name, special_instructions, start])

    db_disconnect(conn)

def cancel_ride(id, name):
    """removes ride from current_rides list this list is for upcoming or ongoing rides"""
    conn, cur = db_connect()
    
    statement = """SELECT * FROM current_rides WHERE rider_id = %s AND r_name = %s """
    cur.execute(statement, [id, name])
    pre = cur.fetchone()

    statement = """DELETE FROM current_rides WHERE rider_id = %s AND r_name = %s"""
    cur.execute(statement, [id, name])

    statement = """SELECT * FROM current_rides WHERE rider_id = %s AND r_name = %s"""
    cur.execute(statement, [id, name])
    post = cur.fetchone()

    db_disconnect(conn)
    return pre, post

def get_new_rider(zipcode):
    """stricly for driver, driver enters their zipcode, all riders in their zipcode are shown"""
    conn, cur = db_connect()

    statement = """SELECT rider_id, name, location, rating FROM rider WHERE zipcode = %s AND wants_ride = true AND is_active = true"""
    cur.execute(statement, [zipcode])
    result = cur.fetchall()
    db_disconnect(conn)
    result = result[0]
    (id, name, start, rating) = result
    return id, name, start, rating

def get_new_drivers(zipcode):
    """rider enters their zipcode, then all availabe drivers are shown"""
    conn, cur = db_connect()

    statement = """SELECT driver_id, name, rating FROM driver WHERE zipcode = %s AND is_active = true"""
    cur.execute(statement, [zipcode])
    result = cur.fetchall()
    db_disconnect(conn)
    result = result[0]
    (id, name, rating) = result
    return id, name, rating

def rider_finish_ride(id, rating_of_driver=4.5, review_of_driver="they were good", timestamp='1999-01-01 00:00:00', carpool = False, cost = 5.0):
    """finishes the riders current ride and adds ride to past rides"""
    conn, cur = db_connect()

    statement = """SELECT * FROM current_rides WHERE rider_id = %s"""
    cur.execute(statement, [id])
    info = cur.fetchone()

    if info != None:
        statement2 = """ INSERT INTO past_rides (d_id, driver_name, r_id, rider_name, special_instructions, start, finish_time, rofd, driver_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(statement2, [info[1], info[2], info[3], info[4], info[5], info[6], timestamp, review_of_driver, rating_of_driver])
        statement = """DELETE FROM current_rides WHERE rider_id = %s"""
        cur.execute(statement, [id])
        charge(id, info[4], cost, timestamp)
        

    #updates the driver rating
    statement = """SELECT (d_id, rider_name) FROM past_rides WHERE r_id = %s"""
    cur.execute(statement, [id])
    result = cur.fetchone()
    result = result[0]
    result = str(result).split(",")
    d_id = str(result[0])
    rider_name = str(result[0].rstrip(")"))
    update_rating("driver", int(d_id[1:]), rating_of_driver)

    if carpool == True:

        statement = """SELECT passengers FROM current_rides WHERE driver_id = %s"""
        cur.execute(statement, [info[1]])
        result = cur.fetchone()

        statement = """UPDATE current_rides SET passengers = passengers - 1 WHERE driver_id = %s"""
        cur.execute(statement, [info[1]])
        charge(id, rider_name, cost/result[0], timestamp)

    db_disconnect(conn)

def driver_finish_ride(id, rid, rating_of_rider=4.5, review_of_rider="they were good", timestamp='1999-01-01 00:00:00', carpool = False, cost = 5.0):
    """driver ends the ride and leaves a rating of the rider"""
    conn, cur = db_connect()

    statement = """SELECT * FROM current_rides WHERE rider_id = %s"""
    cur.execute(statement, [rid])
    info = cur.fetchone()

    if info != None:
        statement2 = """ INSERT INTO past_rides (d_id, driver_name, r_id, rider_name, special_instructions, start, finish_time, rofd, driver_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(statement2, [info[1], info[2], info[3], info[4], info[5], info[6], timestamp, review_of_rider, rating_of_rider])
        
        statement = """DELETE FROM current_rides WHERE rider_id = %s"""
        cur.execute(statement, [rid]) 

        charge(id, info[4], cost, timestamp)
    
    statement = """UPDATE driver SET is_active = true WHERE driver_id = %s"""
    cur.execute(statement, [id])

    #updates the rider rating
    statement = """SELECT (r_id, rider_name) FROM past_rides WHERE d_id = %s"""
    cur.execute(statement, [id])
    result = cur.fetchone()
    result = result[0]
    result = str(result).split(",")
    d_id = str(result[0])
    rider_name = str(result[0].rstrip(")"))
    update_rating("rider", int(d_id[1:]), rating_of_rider)

    if carpool == True:
        statement = """SELECT passengers FROM current_rides WHERE driver_id = %s"""
        cur.execute(statement, [info[1]])
        result = cur.fetchone()

        statement = """UPDATE current_rides SET passengers = passengers - 1 WHERE driver_id = %s"""
        cur.execute(statement, [info[1]])
        charge(id, rider_name, cost/result[0], timestamp)
    db_disconnect(conn)

def get_current_ride(id):
    """gets the info on the current ride of the rider"""
    conn, cur = db_connect()

    statement = """SELECT * FROM current_rides WHERE rider_id = %s """
    cur.execute(statement, [id])   
    result = cur.fetchone()

    db_disconnect(conn)
    return result

def respond(id, role, review):
    """Allows the rider or driver to leave a responce the the rating/review given to them"""
    conn, cur = db_connect()

    if role == "driver":
        statement = """UPDATE past_rides SET d_response = %s WHERE d_id = %s"""
        cur.execute(statement, [review, id])
    else:
        statement = """UPDATE past_rides SET r_response = %s WHERE r_id = %s"""
        cur.execute(statement, [review, id])
    db_disconnect(conn)

def get_reviews(id, role):
    conn, cur = db_connect()

    if role == "driver":
        statement = """SELECT rofd, d_response, rofr, r_response FROM past_rides WHERE d_id = %s """
    else:
        statement = """SELECT rofd, d_response, rofr, r_response FROM past_rides WHERE r_id = %s"""
    
    cur.execute(statement, [id])
    result = cur.fetchall()
    db_disconnect(conn)
    return result

def charge(id, name, amount, timestamp):
    """adds a charge to a list of bills"""
    conn, cur = db_connect()

    statement = """INSERT INTO tab (billed_id, name, charge, timestamp) VALUES (%s, %s, %s, %s)"""
    cur.execute(statement, [id, name, amount, timestamp])
    db_disconnect(conn)

def get_bills(id, name, start = datetime(1, 1, 1), end = datetime(9999, 12, 31)):

    """returns all bills associated with an account"""
    conn, cur = db_connect()

    statement = """SELECT * FROM tab WHERE billed_id = %s AND name = %s AND timestamp > %s AND timestamp < %s"""
    cur.execute(statement, [id, name, start, end])
    result = cur.fetchall()

    statement = """SELECT charge FROM tab WHERE billed_id = %s AND name = %s AND timestamp > %s AND timestamp < %s"""
    cur.execute(statement, [id, name, start, end])
    money = cur.fetchall()
    tablist = [i[0] for i in money]
    tab = fsum(tablist)
    
    db_disconnect(conn)
    return result, tab

def change_carpool(id, zipcode):
    """changes driver's carpool to the opposite of what it was, true -> false || false -> true"""
    conn, cur = db_connect()

    update_zipcode("driver", 1, zipcode)

    statement = """SELECT carpool FROM driver WHERE driver_id = %s"""
    cur.execute(statement, [id])
    wants_carpool = cur.fetchone()
    
    statement = """UPDATE driver SET carpool = %s WHERE driver_id = %s"""
    cur.execute(statement, [not wants_carpool[0], id])

    db_disconnect(conn)

def find_drivers_carpool(zipcode):
    """Finds drivers that are carpooling and aren't full and displays them all, just like finding a driver that isn't carpooling"""
    #LOOKS FOR drivers that are currently giving a carpool, what if there are none currently
    #but tthere are some who ahve no passengerees but are till down to carpool?
    conn, cur = db_connect()
    dlist = []

    statement = """SELECT driver_id FROM driver WHERE carpool = true AND zipcode = %s"""
    cur.execute(statement, [zipcode])
    result = cur.fetchall()
    templist = [x[0] for x in result]

    for i in range(len(templist)):
        statement = """SELECT (d_name, passengers) FROM current_rides WHERE driver_id = %s AND passengers < 4"""
        cur.execute(statement, [templist[i]])
        result = cur.fetchone()
        if result == None:
            return None
        else:
            dlist.append(result[0])
    if len(dlist) == 0:
        for driver in templist:
            dlist.append(get_driver(driver)[1])

    db_disconnect(conn)
    return dlist

def join_carpool(did, dname, rid, rname, instuctions, start, time, zipcode):
    """adds the carpool to the current rides, checks if carpool reaches max of 4 passengers,
       updates every subsequent ride if more are added to the carpool"""
    conn, cur = db_connect()
    statement = """SELECT r_name FROM current_rides WHERE driver_id = %s"""
    cur.execute(statement, [did])
    passengers = cur.fetchall()

    if len(passengers) < 3:
        statement = """INSERT INTO current_rides (driver_id, d_name, rider_id, r_name, s_instructions, start, time, zipcode, passengers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(statement, [did, dname, rid, rname, instuctions, start, time, zipcode, len(passengers)])
        statement = """UPDATE current_rides SET passengers = %s WHERE driver_id = %s"""
        cur.execute(statement, [len(passengers), did])
    
    elif len(passengers) == 3:
        statement = """INSERT INTO current_rides (driver_id, d_name, rider_id, r_name, s_instructions, start, time, zipcode, passengers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(statement, [did, dname, rid, rname, instuctions, start, time, zipcode, 4])
        statement = """UPDATE current_rides SET passengers = %s WHERE driver_id = %s"""
        cur.execute(statement, [4, did])

    db_disconnect(conn)

def full_ride_info(date):
    """displays all rides within one day of given date"""
    conn, cur = db_connect()
    statement = """SELECT (%s)::date"""
    cur.execute(statement, [date])
    date = cur.fetchone()

    statement = """SELECT d_id, driver_name, array_agg(rider_name), avg(driver_rating) FROM past_rides WHERE (finish_time)::date = %s GROUP BY d_id, driver_name ORDER BY d_id, driver_name"""
    cur.execute(statement, [date[0]])
    result = cur.fetchone()

    db_disconnect(conn)
    return result

def fare_times(timestamp):
    """provides all bills charged within the time given"""
    conn, cur = db_connect()

    #trys to turn date into timestamp by adding hour to it
    statement = """SELECT %s - interval '1 hour'"""
    cur.execute(statement, [timestamp])
    starttime = cur.fetchone()
    statement = """SELECT %s + interval '1 hour'"""
    cur.execute(statement, [timestamp])
    endtime = cur.fetchone()

    #uses the bounds tp serch for all bills within constraints
    statement = """SELECT date_part('hour',TIMESTAMP %s)::Integer, AVG(charge) FROM tab WHERE timestamp >= %s AND timestamp <= %s"""
    cur.execute(statement, [timestamp, starttime, endtime])
    result = cur.fetchall()

    db_disconnect(conn)
    return result
