import pymysql

# ---------------- DATABASE SETUP ----------------  #
# Run this file ONCE before starting the main application.
# It creates the database and table if they do not already exist.

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root@7900",
    database="ems_db"       # Database name used throughout the project
)

create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    emp_id      INT            NOT NULL PRIMARY KEY,
    emp_name    VARCHAR(200)   NOT NULL,
    mob_no      VARCHAR(20)    NOT NULL,
    emp_dept    VARCHAR(100),
    emp_salary  DECIMAL(12, 2) DEFAULT 0.00,
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

cur = conn.cursor()
cur.execute(create_table_query)
conn.commit()

cur.close()
conn.close()

print("Database setup complete — table 'employees' is ready in 'ems_db'.")
