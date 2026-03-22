# 🗂️ Employee Management System (EMS)

> **Author:** Aditya Bobade &nbsp;|&nbsp; **Language:** Python 3.8+ &nbsp;|&nbsp; **Database:** MySQL &nbsp;|&nbsp; **License:** Educational Use Only

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Technologies Used](#-technologies-used)
4. [Database Design](#-database-design)
5. [Project Structure](#-project-structure)
6. [Prerequisites](#-prerequisites)
7. [Installation & Setup](#-installation--setup)
8. [Running the Application](#-running-the-application)
9. [Usage Guide](#-usage-guide)
10. [Import / Export File Format](#-import--export-file-format)
11. [Input Validation Rules](#-input-validation-rules)
12. [Known Notes & Tips](#-known-notes--tips)
13. [Contributing](#-contributing)
14. [Need Help?](#-need-help)
15. [License](#-license)

---

## 📌 Project Overview

The **Employee Management System (EMS)** is a full-featured desktop application built using **Python** and **MySQL**. It provides a clean graphical user interface (GUI) built with `tkinter` that allows HR administrators and managers to efficiently manage employee records without writing any SQL manually.

The application supports complete **CRUD operations** (Create, Read, Update, Delete), a dedicated **Salary Management window** with individual salary lookup, **live analytics** across all employee records, and **bulk data import/export** via Excel and CSV files.

All data is stored persistently in a **MySQL database**, meaning records are saved even after the application is closed.

---

## ✅ Features

### Core CRUD Operations
- **Add** new employee records with full field-level input validation
- **View** all employee records in a colour-coded, scrollable Treeview table
- **Select** an employee by ID to automatically pre-fill the update form
- **Update** existing employee details with validation
- **Delete** employee records with a confirmation prompt before deletion
- **Clear** the Treeview display without affecting the database

### Salary Management Window
- Open a dedicated **Salary Management** window from the main interface
- Look up any employee's salary by entering their Employee ID
- View formatted salary output with the employee's name

### Analytics Dashboard
- View live **Employee Analytics** including:
  - Total number of employees
  - Average salary across all employees
  - Highest salary in the organisation
  - Lowest salary in the organisation

### Import & Export
- **Import from Excel** (`.xlsx` / `.xls`) — bulk insert employees from a spreadsheet
- **Import from CSV** (`.csv`) — bulk insert employees from a CSV file
- **Export to Excel** (`.xlsx`) — save all employee records to a spreadsheet
- **Export to CSV** (`.csv`) — save all employee records to a CSV file
- **Duplicate-safe import** — if an Employee ID already exists in the database, that row is skipped gracefully and counted separately

### UI / UX
- Background image support for both the main window and salary window
- Alternating row colours in the Treeview for easy reading
- Column resize and heading click are blocked to keep the table stable
- Combobox dropdown for Department selection (prevents typos)
- All buttons styled consistently with ridge relief

---

## 🛠️ Technologies Used

| Component        | Technology / Library         | Purpose                                      |
|------------------|------------------------------|----------------------------------------------|
| Language         | Python 3.8+                  | Core application logic                       |
| GUI Framework    | `tkinter` + `ttk`            | All windows, widgets, forms, and Treeview    |
| Database         | MySQL                        | Persistent storage of employee records       |
| DB Connector     | `pymysql`                    | Python-to-MySQL connection and queries       |
| Data Handling    | `pandas`                     | Reading/writing Excel and CSV files          |
| Excel Support    | `openpyxl`                   | Required by pandas for `.xlsx` files         |
| Image Handling   | `Pillow` (PIL)               | Loading and resizing background images       |
| IDE              | VS Code / PyCharm            | Recommended development environment          |

---

## 🗄️ Database Design

**Database name:** `ems_db`

**Table name:** `employees`

| Column Name  | Data Type         | Constraint                  | Description                                                     |
|--------------|-------------------|-----------------------------|-----------------------------------------------------------------|
| `emp_id`     | `INT`             | `PRIMARY KEY`, `NOT NULL`   | Unique employee ID — entered manually by the user               |
| `emp_name`   | `VARCHAR(200)`    | `NOT NULL`                  | Full name of the employee                                       |
| `mob_no`     | `VARCHAR(20)`     | `NOT NULL`                  | 10-digit mobile number stored as text                           |
| `emp_dept`   | `VARCHAR(100)`    | —                           | Department (Finance, Marketing, Production, HR, IT, Sales)      |
| `emp_salary` | `DECIMAL(12, 2)`  | `DEFAULT 0.00`              | Monthly gross salary                                            |
| `created_at` | `TIMESTAMP`       | `DEFAULT CURRENT_TIMESTAMP` | Automatically set when the record is first created              |
| `updated_at` | `TIMESTAMP`       | `AUTO on UPDATE`            | Automatically updated whenever the record is modified           |

> **Note:** `created_at` and `updated_at` are handled entirely by MySQL.
> The Python application only inserts the five core columns — these two timestamps are set and updated automatically by the database engine.

---

## 📁 Project Structure

```
C:\Aditya's Projects\EmployeeHub\
│
├── EMS_project.py           →  Main application — all GUI, logic, and database operations
├── EMS_pymysql_setup.py     →  One-time setup script — creates the "employees" table in MySQL
├── EMS_database_setup.sql   →  MySQL script — manual alternative to the Python setup script
├── README.md                →  Project documentation (this file)
├── .gitignore               →  Git ignore rules — excludes cache, venv, IDE files
│
└── assets\
        bg.png               →  Background image for the main window (1920x1080)
        bg2.png              →  Background image for the Salary Management window (1920x992)
```

---

## 📦 Prerequisites

Make sure the following are installed on your system before running the project:

| Requirement  | Version      | Download Link                                      |
|--------------|--------------|----------------------------------------------------|
| Python       | 3.8 or above | https://www.python.org/downloads/                  |
| MySQL Server | 5.7 or above | https://dev.mysql.com/downloads/mysql/             |
| pip          | Latest       | Comes bundled with Python                          |

---

## ⚙️ Installation & Setup

### Step 1 — Install Python
Download and install Python 3.8 or above from [python.org](https://www.python.org/downloads/).
During installation, make sure to check **"Add Python to PATH"**.

---

### Step 2 — Install required Python libraries
Open **Windows PowerShell** and run:

```powershell
pip install pymysql pandas pillow openpyxl
```

This installs all four required libraries in one command.

| Library    | What it does                                      |
|------------|---------------------------------------------------|
| `pymysql`  | Connects Python to your MySQL database            |
| `pandas`   | Reads and writes Excel and CSV files              |
| `pillow`   | Loads and resizes background images in the GUI    |
| `openpyxl` | Required by pandas to handle `.xlsx` Excel files  |

---

### Step 3 — Install and configure MySQL
1. Download and install **MySQL Community Server** from [dev.mysql.com](https://dev.mysql.com/downloads/mysql/)
2. During installation, set a root password (the project uses `root@7900` by default — you can change this later)
3. Ensure the MySQL service is running before launching the application

---

### Step 4 — Create the database
Open **MySQL Workbench** or the **MySQL command line** and run:

```sql
CREATE DATABASE IF NOT EXISTS ems_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;
```

---

### Step 5 — Create the employees table

**Option A — Using the Python setup script (recommended):**

Open **Windows PowerShell**, navigate to the project folder and run:

```powershell
cd "C:\Aditya's Projects\EmployeeHub"
python EMS_pymysql_setup.py
```

You should see this output:
```
Database setup complete — table 'employees' is ready in 'ems_db'.
```

**Option B — Using the SQL script manually:**

Open `EMS_database_setup.sql` in MySQL Workbench and execute the entire script.
It will create the `employees` table with all columns and constraints.

---

### Step 6 — Configure database credentials
Open `EMS_project.py` and find the `get_connection()` function near the top of the file:

```python
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root@7900",   # ← change this to your MySQL root password
        database="ems_db"
    )
```

Update the `password` value to match whatever password you set during MySQL installation.

---

### Step 7 — Background images
The background images are already placed in the correct location:

```
C:\Aditya's Projects\EmployeeHub\assets\bg.png
C:\Aditya's Projects\EmployeeHub\assets\bg2.png
```

Make sure the image paths referenced inside `EMS_project.py` point to this `assets\` folder.
If the images are missing or the path is wrong, the app will automatically fall back to a plain **light-blue background** — it will not crash.

---

## ▶️ Running the Application

Open **Windows PowerShell**, navigate to the project folder, and run the main file:

```powershell
cd "C:\Aditya's Projects\EmployeeHub"
python EMS_project.py
```

The main EMS window will open in **fullscreen (zoomed)** mode automatically.

---

## 📖 Usage Guide

### Main Window

#### ➕ Adding an Employee
1. Fill in all five input fields: **Employee ID**, **Employee Name**, **Mobile Number**, **Department**, **Salary**
2. Select a department from the dropdown menu
3. Click **ADD**
4. A success message will confirm the record was saved, and all fields will be cleared automatically

#### 👁️ Viewing All Employees
- Click **SHOW** to load all employee records from the database into the Treeview table
- Rows display with alternating colours (white and light blue-grey) for easy reading

#### 🗑️ Deleting an Employee
1. Enter the Employee ID in the **ENTER ID TO DELETE** field
2. Click **DELETE**
3. A confirmation dialog appears — click **Yes** to confirm or **No** to cancel
4. If the ID does not exist in the database, a "Not Found" warning is shown

#### ✏️ Updating an Employee
1. Enter the Employee ID in the **UPDATE EMP INFO** field
2. Click **SELECT** — the employee's current details will automatically fill into the top five input fields
3. Edit whichever fields you want to change
4. Click **UPDATE** to save the changes to the database

#### 🧹 Clearing the Table View
- Click **CLEAR** to remove all rows from the Treeview display
- This does **not** delete any data from the database — it only clears the visual table

---

### Salary Management Window

1. Click the **SALARY** button on the main window — a new dedicated window opens
2. Enter an Employee ID in the input field
3. Click **SHOW SALARY** to display that employee's full name and current salary
4. Click **SHOW ANALYTICS** to view organisation-wide salary statistics:
   - Total number of employees
   - Average salary (formatted with 2 decimal places)
   - Highest salary
   - Lowest salary

---

### Import & Export

#### Importing Data (Bulk Insert)
1. Click **IMPORT EXCEL FILE** or **IMPORT CSV FILE**
2. A file browser dialog will open — navigate to and select your file
3. The application validates that all required column headers are present
4. All valid rows are inserted into the database and displayed in the Treeview
5. Any rows with duplicate Employee IDs are automatically skipped
6. A success message shows how many records were inserted and how many were skipped

#### Exporting Data
1. Click **EXPORT EXCEL FILE** or **EXPORT CSV FILE**
2. A save dialog will open — choose your destination folder and enter a filename
3. All current records from the database are written to the chosen file format
4. A success message confirms the export and shows the full file path

---

## 📄 Import / Export File Format

Your import files **must** have these exact column header names (spelling and capitalisation matter):

| ID  | Name          | Mobile No  | Department | Salary |
|-----|---------------|------------|------------|--------|
| 101 | Aditya Bobade | 9876543210 | IT         | 75000  |
| 102 | Rahul Sharma  | 8765432109 | HR         | 55000  |
| 103 | Priya Patil   | 7654321098 | Finance    | 62000  |

> ⚠️ **Important:** Column headers must be exactly `ID`, `Name`, `Mobile No`, `Department`, `Salary`.
> Any spelling difference or missing column will cause an error message and the import will be cancelled.

---

## ✔️ Input Validation Rules

The application enforces the following rules before saving or updating any record:

| Field         | Rule                                                                        |
|---------------|-----------------------------------------------------------------------------|
| Employee ID   | Must be a positive whole number — no letters, no zero, cannot be blank      |
| Employee Name | Letters, spaces, and dots only — no numbers or special characters           |
| Mobile Number | Exactly 10 digits, numbers only — no spaces or dashes                       |
| Department    | Must be selected from the dropdown (Finance, Marketing, Production, HR, IT, Sales) |
| Salary        | Must be a positive whole number — no negative values                        |

If any field fails validation, a descriptive error message is shown and the record is **not** saved until all fields are corrected.

---

## 💡 Known Notes & Tips

- **Background image memory** — The app stores a reference to the background image on the window object (`win.bg_image = bg_image`) to prevent Python's garbage collector from deleting it from memory mid-session. Without this, the background would randomly disappear while the app is running. This is a well-known tkinter behaviour.

- **Toplevel window** — The Salary Management window uses `Toplevel()` and shares the main application's event loop. It does **not** call `mainloop()` separately — doing so would freeze the main window.

- **Parameterized queries** — All database queries use `%s` placeholders instead of f-string formatting. This protects the application against SQL injection attacks.

- **Duplicate imports** — If you import a file that contains Employee IDs already in the database, those rows are caught via `IntegrityError` and skipped. The success message always reports both inserted and skipped counts.

- **Table name** — The correct MySQL table name in this project is `employees`. Any references to `emp_db` as a table name in older versions of this project were a bug — all queries now use `employees`.

- **No AUTO_INCREMENT** — Employee IDs are entered manually by the user. There is no auto-increment on `emp_id` by design, as the system is intended for organisations with their own employee ID numbering scheme.

---

## 🤝 Contributing

Contributions are welcome for learning and improvement purposes.

1. Fork this repository
2. Create a new feature branch:
```powershell
git checkout -b feature/your-feature-name
```
3. Make your changes and write a clear commit message:
```powershell
git commit -m "Add: description of what you added or fixed"
```
4. Push your branch:
```powershell
git push origin feature/your-feature-name
```
5. Open a **Pull Request** and describe what you changed and why

---

## 📞 Need Help?

If you have any questions, suggestions, or run into any issues with this project, feel free to reach out:

| Platform    | Link                                                                          |
|-------------|-------------------------------------------------------------------------------|
| 💼 LinkedIn  | [linkedin.com/in/adityabobade](https://linkedin.com/in/adityabobade)          |
| 📧 Email     | [bobade1436@gmail.com](mailto:bobade1436@gmail.com)                           |

---

## 📜 License

```
Copyright © 2025 Aditya Bobade

This project is intended for EDUCATIONAL PURPOSES ONLY.
You may use, modify, and share this project for learning or personal research.
Commercial use, selling, or redistribution for profit is strictly NOT permitted.
All rights reserved.
```
Made with ❤️, fueled by ☕