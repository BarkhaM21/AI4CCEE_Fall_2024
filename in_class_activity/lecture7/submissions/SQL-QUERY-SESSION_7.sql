-- ACTIVITY 1 - CREATE TABLES 

-- DROP TABLE IF EXISTS gps_data;

-- CREATE TABLE gps_data (
--     datapointid VARCHAR(40) PRIMARY KEY,
--     journeyid VARCHAR(40),
--     latitude NUMERIC(10, 7),
--     longitude NUMERIC(10, 7),
--     month INTEGER,
--     day INTEGER,
--     hour INTEGER
-- );

-- COPY gps_data (datapointid, journeyid, latitude, longitude, month, day, hour)
-- FROM 'C:/adi10136/Documents/CE-5900-16/gps_data.csv'
-- DELIMITER ',' 
-- CSV HEADER;


-- DROP TABLE IF EXISTS vehicle_data;

-- CREATE TABLE vehicle_data (
--     datapointid VARCHAR(40) PRIMARY KEY,
--     geohash VARCHAR(12),
--     speed NUMERIC(5, 2),
--     make VARCHAR(50),
--     model VARCHAR(50),
--     route_id VARCHAR(20),
--     segment_start_measure NUMERIC(10, 3)
-- );

-- COPY vehicle_data (datapointid, geohash, speed, make, model, route_id, segment_start_measure)
-- FROM 'C:/adi10136/Documents/CE-5900-16/vehicle_data.csv'
-- DELIMITER ',' 
-- CSV HEADER;

------------------------------------------------------------------------------------------------------------

-- ACTIVITY 2

-- SELECT *
-- FROM gps_data
-- WHERE month = 10 AND day = 3 AND hour = 4;


-- SELECT COUNT(*)
-- FROM gps_data

-- SELECT COUNT(DISTINCT journeyid)
-- FROM gps_data
-- WHERE month = 10 AND day = 3 AND hour = 4; 

-- -- Query to select the rows
-- SELECT *
-- FROM gps_data
-- WHERE month = 10 AND day IN (1, 3) AND hour BETWEEN 3 AND 6;

-- -- Query to count the rows that match the condition
-- SELECT COUNT(*)
-- FROM gps_data
-- WHERE month = 10 AND day IN (1, 3) AND hour BETWEEN 3 AND 6;



-- SELECT COUNT(*)
-- FROM gps_data
-- WHERE month = 10 AND day IN (1, 3);

-- SELECT hour, COUNT(*)
-- FROM gps_data
-- WHERE month = 10 AND day IN (1, 3) AND hour BETWEEN 3 AND 6
-- GROUP BY hour
-- ORDER BY hour;


-- -- SELECT *
-- -- FROM gps_data
-- -- WHERE month = 10 AND day IN (1, 3) AND hour BETWEEN 3 AND 6;


-- SELECT DISTINCT journeyid
-- FROM gps_data
-- WHERE journeyid LIKE '%abc%';


-- SELECT COUNT(*)
-- FROM gps_data
-- WHERE datapointid LIKE '9%';

-- SELECT *
-- FROM gps_data
-- WHERE journeyid LIKE '%cc';

-- SELECT *, CONCAT(datapointid, '-', day) AS dpid_day
-- FROM gps_data;

------------------------------------------------------------------------------------------------------------------

-- ACTIVITY - 3 - Aggregations

-- SELECT MAX(speed) AS max_speed
-- FROM vehicle_data;

-- SELECT 
--     AVG(speed) AS avg_speed,
--     MIN(speed) AS min_speed,
--     MAX(speed) AS max_speed,
--     STDDEV(speed) AS stddev_speed
-- FROM vehicle_data
-- WHERE make = 'CHEVROLET';

-- SELECT 
--     route_id || '-' || segment_start_measure AS seg_id,
--     *
-- FROM vehicle_data;

-- ALTER TABLE vehicle_data
-- ADD COLUMN seg_id VARCHAR(60);

-- UPDATE vehicle_data
-- SET seg_id = route_id || '-' || segment_start_measure;

-- SELECT seg_id, *
-- FROM vehicle_data
-- LIMIT 10;

-- SELECT 
--     seg_id,
--     percentile_cont(0.85) WITHIN GROUP (ORDER BY speed) AS percentile_85_speed
-- FROM vehicle_data
-- GROUP BY seg_id;

-- SELECT 
--     model,
--     MAX(speed) AS max_speed
-- FROM vehicle_data
-- GROUP BY model;

-- SELECT 
--     model,
--     percentile_cont(0.95) WITHIN GROUP (ORDER BY speed) AS percentile_95_speed
-- FROM vehicle_data
-- GROUP BY model;

------------------------------------------------------------------------------------------------------------------

-- ACTIVITY - 4 : Joins

-- SELECT *
-- FROM gps_data
-- JOIN vehicle_data ON gps_data.datapointid = vehicle_data.datapointid;

-- SELECT gps_data.datapointid, gps_data.journeyid, vehicle_data.speed, vehicle_data.seg_id
-- FROM gps_data
-- JOIN vehicle_data ON gps_data.datapointid = vehicle_data.datapointid;

-- SELECT COUNT(DISTINCT gps_data.journeyid) AS stopped_journey_count
-- FROM gps_data
-- JOIN vehicle_data ON gps_data.datapointid = vehicle_data.datapointid
-- WHERE vehicle_data.speed = 0;
