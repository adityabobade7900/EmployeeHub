-- ================================================================
--  Employee Management System — Database Setup Script
--  Author : Aditya Bobade
--  Run this script once in MySQL before starting the application.
-- ================================================================


-- ----------------------------------------------------------------
-- 1. Create database
-- ----------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS ems_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE ems_db;


-- ----------------------------------------------------------------
-- 2. Create table
--    Table name : employees (standardised everywhere)
--    emp_id     : manual entry — no AUTO_INCREMENT by design
--    created_at / updated_at : handled automatically by MySQL
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employees (
    emp_id      INT            NOT NULL PRIMARY KEY,
    emp_name    VARCHAR(200)   NOT NULL,
    mob_no      VARCHAR(20)    NOT NULL,
    emp_dept    VARCHAR(100),
    emp_salary  DECIMAL(12, 2) DEFAULT 0.00,
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- ----------------------------------------------------------------
-- 3. Quick sanity checks (optional — run manually if needed)
-- ----------------------------------------------------------------
SHOW TABLES;

DESCRIBE employees;

SELECT * FROM employees;


-- ----------------------------------------------------------------
-- 4. Example data operations
-- ----------------------------------------------------------------

-- Insert a sample employee
INSERT INTO employees (emp_id, emp_name, mob_no, emp_dept, emp_salary)
VALUES (101, 'Aditya Bobade', '9876543210', 'IT', 75000.00);

-- Update mobile number for a specific employee
UPDATE employees
SET mob_no = '8010502680'
WHERE emp_id = 117;

-- Delete an employee record
DELETE FROM employees
WHERE emp_id = 101;

-- ================================================================
-- END OF SETUP SCRIPT
-- ================================================================
