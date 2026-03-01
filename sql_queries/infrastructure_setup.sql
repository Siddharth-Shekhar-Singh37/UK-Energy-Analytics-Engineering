-- 1. Create the Database for our project
CREATE DATABASE IF NOT EXISTS UK_ENERGY_DB;

-- 2. Create the RAW Schema (the Landing Zone for data)
CREATE SCHEMA IF NOT EXISTS UK_ENERGY_DB.RAW;

-- 3. Create the ENERGY_WH Warehouse (The Engine)
CREATE WAREHOUSE IF NOT EXISTS ENERGY_WH 
WITH WAREHOUSE_SIZE = 'XSMALL' 
AUTO_SUSPEND = 60 
AUTO_RESUME = TRUE;
SHOW DATABASES;

-- Check the total row count
SELECT COUNT(*) as total_rows FROM UK_ENERGY_DB.RAW.LONDON_ENERGY_RAW;

-- Take a look at the data structure
SELECT * FROM UK_ENERGY_DB.RAW.LONDON_ENERGY_RAW LIMIT 10;
