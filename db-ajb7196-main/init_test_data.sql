--drivers
INSERT INTO "driver" ("name", "rating", "special_instructions", "birthday", "zipcode") VALUES
    ('Ray Magliozzi', 3.2, 'Dont drive like my brother.', '1995-10-16', '94131'),
    ('Tom Magliozzi', 3.4, 'Dont drive like my brother.', '1995-10-15', '30301');

--riders
INSERT INTO "rider" ("name", "rating", "birthday") VALUES
    ('Mike Easter', 4.3, '1994-5-27'),
    ('Ayden Boyko', 4.5, '2003-11-24');

--past_rides
INSERT INTO "past_rides" ("d_id", "driver_name", "r_id", "rider_name", "rofd") VALUES
    (1, 'Ray Magliozzi', 1, 'Mike Easter', 'hes a good driver'),
    (2, 'Tom Magliozzi', 1, 'Ray Magliozzi', 'He drove better than his brother, haha');
    

INSERT INTO "current_rides" ("driver_id", "d_name", "rider_id", "r_name") VALUES
    (1, 'Ray Magliozzi', 2, 'Ayden Boyko');

INSERT INTO "tab" ("billed_id", "name", "charge") VALUES
    (1, 'Mike Easter', 5.00),
    (1, 'Mike Easter', 4.50);