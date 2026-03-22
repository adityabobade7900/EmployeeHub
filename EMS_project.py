# ---------------- This Is Made By Aditya Bobade ----------------  #

import tkinter as tk
from tkinter import Toplevel, messagebox, ttk, Button, CENTER, Tk, Label, Entry, StringVar, filedialog
from PIL import Image, ImageTk
import pymysql
import re
import pandas as pd

# ---------------- DATABASE CONNECTION ----------------  #


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root@7900",
        database="ems_db"
    )


# ---------------- CRUD OPERATIONS ----------------  #


def show_data():
    view.delete(*view.get_children())
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, emp_name, mob_no, emp_dept, emp_salary FROM employees")
        rows = cursor.fetchall()

        # Insert rows with alternating colors
        for index, row in enumerate(rows):
            if index % 2 == 0:
                view.insert("", "end", values=row, tags=("evenrow",))
            else:
                view.insert("", "end", values=row, tags=("oddrow",))

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def exit_program():
    win.destroy()


def add_data():
    emp_id = id1.get().strip()
    emp_name = id2.get().strip()
    mob_no = id3.get().strip()
    emp_dept = id4.get().strip()
    emp_salary = id5.get().strip()

    # Validation
    if emp_id == '' or emp_name == '' or mob_no == '' or emp_dept == '' or emp_salary == '':
        messagebox.showinfo('Info', 'ALL fields are compulsory')

    elif not emp_id.isdigit() or int(emp_id) <= 0:
        messagebox.showerror("Error", "Employee ID must be a positive number")

    elif not re.match(r'^[A-Za-z .]+$', emp_name):
        messagebox.showerror(
            "Error", "Employee Name must contain only letters and spaces")

    elif not re.match(r'^[A-Za-z ]+$', emp_dept):
        messagebox.showerror(
            "Error", "Employee Department must contain only letters and spaces")

    elif not mob_no.isdigit() or len(mob_no) != 10:
        messagebox.showerror("Error", "Mobile Number must be 10 digits")

    elif not emp_salary.isdigit() or int(emp_salary) <= 0:
        messagebox.showerror(
            "Error", "Employee Salary must be a positive number")

    else:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employees (emp_id, emp_name, mob_no, emp_dept, emp_salary) VALUES (%s, %s, %s, %s, %s)",
                (emp_id, emp_name, mob_no, emp_dept, emp_salary)
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Data Inserted Successfully")

            # Clear input fields
            id1.set("")
            id2.set("")
            id3.set("")
            id4.set("")
            id5.set("")

        except pymysql.err.IntegrityError:
            messagebox.showerror(
                "Error", f"Employee ID {emp_id} already exists")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ---------------- SALARY MANAGEMENT ----------------  #


def show_salary():
    global win2
    win2 = Toplevel()
    win2.title("Salary Management")
    win2.config(bg="lightblue")
    win2.geometry("1920x1080")

    # Load and set background image
    try:
        image = Image.open(r"C:\Aditya's Projects\EmployeeHub\assets\bg2.png")
        image = image.resize((1920, 992), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label = Label(win2, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()
        win2.bg_image = bg_image
    except Exception:
        pass  # If background image not found, continue without it

    # emp_id >> Label
    l8 = Label(
        win2,
        text="ENTER EMPLOYEE ID",
        bg="white",
        fg="black",
        width=20,
        bd=7,
        relief="ridge",
        font=("times new roman", 12, "bold")
    )
    l8.place(x=450, y=250)

    # emp_id >>> entry
    id8 = StringVar()
    e8 = Entry(
        win2,
        textvariable=id8,
        bg="white",
        width=25,
        bd=5,
        relief="flat",
        font=("times new roman", 12, "bold")
    )
    e8.place(x=700, y=255)
    e8.configure(justify="center")

    # label to display salary
    result_label = Label(
        win2,
        text="",
        font=("Times New Roman", 14, "bold"),
        bg="white",
        fg="black",
        relief="ridge",
        width=34,
        height=5,
        bd=8,
    )
    result_label.place(x=450, y=340)

    # SHOW SALARY button
    b9 = Button(
        win2,
        text="SHOW SALARY",
        command=lambda: show_sal(id8.get(), result_label),
        relief="ridge",
        bg="gray",
        fg="white",
        bd=4,
        font=("times new roman", 12, "bold"),
        width=15,
    )
    b9.place(x=450, y=500)

    # SHOW ANALYTICS button
    b10 = Button(
        win2,
        text="SHOW ANALYTICS",
        command=show_analytics,
        relief="ridge",
        bg="gray",
        fg="white",
        bd=4,
        font=("times new roman", 12, "bold"),
        width=15,
    )
    b10.place(x=1000, y=500)


def show_analytics():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*), AVG(emp_salary), MAX(emp_salary), MIN(emp_salary) FROM employees")
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is not None and result[0]:
        total_employees, avg_salary, max_salary, min_salary = result
    else:
        total_employees, avg_salary, max_salary, min_salary = 0, 0.0, 0, 0

    Label(
        win2,
        text="Employee Analytics",
        bg="white",
        fg="black",
        width=25,
        bd=5,
        relief="ridge",
        font=("Times New Roman", 18, "bold"),
    ).place(x=1000, y=250)

    Label(
        win2,
        text=f"Total Employees: {int(total_employees)}\n"
        f"Average Salary:  {float(avg_salary):,.2f}\n"
        f"Highest Salary:  {int(max_salary):,}\n"
        f"Lowest Salary:   {int(min_salary):,}",
        font=("Times New Roman", 14),
        bg="white",
        fg="black",
        relief="ridge",
        width=34,
        height=5,
        bd=8,
        justify="left",
    ).place(x=1000, y=340)


def show_sal(emp_id, result):
    if emp_id == "":
        result.config(text="Please enter an Employee ID")
        return
    elif not emp_id.isdigit():
        result.config(text="Please enter a valid numeric Employee ID")
        return

    emp_id = int(emp_id)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT emp_name, emp_salary FROM employees WHERE emp_id=%s", (emp_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        emp_name, emp_salary = row
        emp_name = emp_name.title()
        result.config(text=f"Salary of {emp_name} is:  {emp_salary:,.2f}")
    else:
        result.config(text="Employee not found")


# ---------------- DELETE OPERATION ----------------  #


def delete_data():
    emp_id = id6.get().strip()
    if emp_id == "":
        messagebox.showerror("Error", "Employee ID is required")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete", f"Are you sure you want to delete Employee ID {emp_id}?")

    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()

            if affected:
                messagebox.showinfo(
                    "Success", f"Employee ID {emp_id} deleted successfully")
            else:
                messagebox.showwarning(
                    "Not Found", f"No employee found with ID {emp_id}")
            id6.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("Cancelled", "Delete operation cancelled")


# ---------------- SELECT OPERATION ----------------  #


def select_emp():
    emp_id = id7.get().strip()
    if emp_id == "":
        messagebox.showerror("Error", "Employee ID is required")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, emp_name, mob_no, emp_dept, emp_salary FROM employees WHERE emp_id=%s",
            (emp_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            id1.set(row[0])
            id2.set(row[1])
            id3.set(row[2])
            id4.set(row[3])
            id5.set(row[4])
        else:
            messagebox.showwarning("Not Found", "Employee not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UPDATE OPERATION ----------------  #


def update_data():
    emp_id = id1.get().strip()
    emp_name = id2.get().strip()
    mob_no = id3.get().strip()
    emp_dept = id4.get().strip()
    emp_salary = id5.get().strip()

    # Validation
    if emp_id == '' or emp_name == '' or mob_no == '' or emp_dept == '' or emp_salary == '':
        messagebox.showinfo('Info', 'ALL fields are compulsory')

    elif not emp_id.isdigit():
        messagebox.showerror("Error", "Employee ID must be a number")

    elif not re.match(r'^[A-Za-z .]+$', emp_name):
        messagebox.showerror(
            "Error", "Employee Name must contain only letters, spaces, and dots")

    elif not re.match(r'^[A-Za-z .]+$', emp_dept):
        messagebox.showerror(
            "Error", "Employee Department must contain only letters, spaces, and dots")

    elif not mob_no.isdigit() or len(mob_no) != 10:
        messagebox.showerror("Error", "Mobile Number must be 10 digits")

    elif not emp_salary.isdigit() or int(emp_salary) <= 0:
        messagebox.showerror(
            "Error", "Employee Salary must be a positive number")

    else:
        try:
            conn = get_connection()
            mycur = conn.cursor()
            mycur.execute(
                "UPDATE employees SET emp_name=%s, mob_no=%s, emp_dept=%s, emp_salary=%s WHERE emp_id=%s",
                (emp_name, mob_no, emp_dept, emp_salary, emp_id)
            )
            conn.commit()
            affected = mycur.rowcount
            mycur.close()
            conn.close()

            if affected:
                messagebox.showinfo('Success', 'Data updated successfully')
            else:
                messagebox.showwarning(
                    "Not Found", f"No employee found with ID {emp_id}")

            # Clear fields
            id1.set('')
            id2.set('')
            id3.set('')
            id4.set('')
            id5.set('')
            id7.set('')

        except Exception as e:
            messagebox.showerror("Error", str(e))


def clear_data():
    view.delete(*view.get_children())


# ----------- IMPORT EXCEL FILE -----------


def import_excel():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return

        df = pd.read_excel(file_path)

        required_cols = ["ID", "Name", "Mobile No", "Department", "Salary"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            messagebox.showerror(
                "Error", f"Missing columns: {', '.join(missing)}")
            return

        view.delete(*view.get_children())

        conn = get_connection()
        cursor = conn.cursor()

        inserted = 0
        skipped = 0
        for _, row in df.iterrows():
            emp_id = row["ID"]
            emp_name = row["Name"]
            emp_mob = row["Mobile No"]
            emp_dept = row["Department"]
            emp_sal = row["Salary"]

            try:
                cursor.execute(
                    "INSERT INTO employees (emp_id, emp_name, mob_no, emp_dept, emp_salary) VALUES (%s, %s, %s, %s, %s)",
                    (emp_id, emp_name, emp_mob, emp_dept, emp_sal)
                )
                view.insert("", "end", values=(
                    emp_id, emp_name, emp_mob, emp_dept, emp_sal))
                inserted += 1
            except pymysql.err.IntegrityError:
                skipped += 1  # Skip duplicate IDs gracefully

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo(
            "Success", f"Import complete: {inserted} inserted, {skipped} skipped (duplicates)")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------- IMPORT CSV FILE -----------


def import_csv():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        df = pd.read_csv(file_path)

        required_cols = ["ID", "Name", "Mobile No", "Department", "Salary"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            messagebox.showerror(
                "Error", f"Missing columns: {', '.join(missing)}")
            return

        view.delete(*view.get_children())

        conn = get_connection()
        cursor = conn.cursor()

        inserted = 0
        skipped = 0
        for _, row in df.iterrows():
            emp_id = row["ID"]
            emp_name = row["Name"]
            emp_mob = row["Mobile No"]
            emp_dept = row["Department"]
            emp_sal = row["Salary"]

            try:
                cursor.execute(
                    "INSERT INTO employees (emp_id, emp_name, mob_no, emp_dept, emp_salary) VALUES (%s, %s, %s, %s, %s)",
                    (emp_id, emp_name, emp_mob, emp_dept, emp_sal)
                )
                view.insert("", "end", values=(
                    emp_id, emp_name, emp_mob, emp_dept, emp_sal))
                inserted += 1
            except pymysql.err.IntegrityError:
                skipped += 1

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo(
            "Success", f"CSV import complete: {inserted} inserted, {skipped} skipped (duplicates)")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------- EXPORT EXCEL FILE -----------


def export_excel():
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, emp_name, mob_no, emp_dept, emp_salary FROM employees")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        columns = ["ID", "Name", "Mobile No", "Department", "Salary"]
        df = pd.DataFrame(rows, columns=columns)
        df.to_excel(file_path, index=False)

        messagebox.showinfo(
            "Success", f"Data exported successfully to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------- EXPORT CSV FILE ----------------


def export_csv():
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, emp_name, mob_no, emp_dept, emp_salary FROM employees")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        columns = ["ID", "Name", "Mobile No", "Department", "Salary"]
        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(file_path, index=False)

        messagebox.showinfo(
            "Success", f"Data exported successfully to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI SECTION ----------------


win = Tk()
win.title("Employee Management System")

# Background image — wrapped in try/except so app still runs if image is missing
try:
    image = Image.open(r"C:\Aditya's Projects\EmployeeHub\assets\bg.png")
    image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = Label(win, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    win.bg_image = bg_image
except Exception:
    win.config(bg="lightblue")
    # dummy label so bg_label.lower() below doesn't crash
    bg_label = Label(win)

# ---------------- This Is Made By Aditya Bobade ----------------  #

# Main Heading Label
l0 = Label(
    win,
    text="◈  EMPLOYEE  MANAGEMENT  SYSTEM  ◈",
    bg="white",
    fg="black",
    width=40,
    bd=8,
    relief="ridge",
    font=("Georgia Bold", 17)
)
l0.pack(anchor="center", pady=40)

# ---------- EMPLOYEE ID ----------

l1 = Label(win, text="EMPLOYEE ID", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l1.place(x=100, y=102)

id1 = StringVar()
e1 = Entry(win, textvariable=id1, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e1.place(x=330, y=105)
e1.configure(justify="center")

# ---------- EMPLOYEE NAME ----------

l2 = Label(win, text="EMPLOYEE NAME", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l2.place(x=100, y=152)

id2 = StringVar()
e2 = Entry(win, textvariable=id2, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e2.place(x=330, y=155)
e2.configure(justify="center")

# ---------- MOBILE NUMBER ----------

l3 = Label(win, text="MOBILE NUMBER", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l3.place(x=100, y=202)

id3 = StringVar()
e3 = Entry(win, textvariable=id3, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e3.place(x=330, y=200)
e3.configure(justify="center")

# ---------- DEPARTMENT ----------

l4 = Label(win, text="DEPARTMENT", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l4.place(x=100, y=253)

id4 = StringVar()
e4 = ttk.Combobox(win, textvariable=id4, width=39,
                  font=("times new roman", 12, "bold"),
                  values=["Finance", "Marketing",
                          "Production", "HR", "IT", "Sales"],
                  state="readonly")
e4.place(x=330, y=250, height=35)
e4.current(0)
e4.configure(justify="center")

# ---------- SALARY ----------

l5 = Label(win, text="SALARY", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l5.place(x=100, y=300)

id5 = StringVar()
e5 = Entry(win, textvariable=id5, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e5.place(x=330, y=300)
e5.configure(justify="center")

# ---------- BUTTONS: SHOW / EXIT / ADD / SALARY ----------

b1 = Button(win, text="SHOW", command=show_data,
            relief="ridge", bd=4, bg="gray", fg="white",
            font=("times new roman", 12, "bold"), width=15)
b1.place(x=190, y=370)

b2 = Button(win, text="EXIT PROGRAM", command=exit_program,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b2.place(x=190, y=420)

b3 = Button(win, text="ADD", command=add_data,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b3.place(x=400, y=370)

b4 = Button(win, text="SALARY", command=show_salary,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b4.place(x=400, y=420)

# ---------- DELETE SECTION ----------

l6 = Label(win, text="ENTER ID TO DELETE", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l6.place(x=100, y=485)

id6 = StringVar()
e6 = Entry(win, textvariable=id6, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e6.place(x=330, y=490)
e6.configure(justify="center")

b5 = Button(win, text="DELETE", command=delete_data,
            relief="ridge", bg="#FF7F7F", fg="black", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b5.place(x=300, y=555)

# ---------- UPDATE SECTION ----------

l7 = Label(win, text="UPDATE EMP INFO", bg="white", fg="black",
           width=20, bd=7, relief="ridge", font=("times new roman", 12, "bold"))
l7.place(x=100, y=620)

id7 = StringVar()
e7 = Entry(win, textvariable=id7, bg="white", width=40, bd=5,
           relief="flat", font=("times new roman", 12, "bold"))
e7.place(x=330, y=625)
e7.configure(justify="center")

b6 = Button(win, text="SELECT", command=select_emp,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b6.place(x=190, y=695)

b7 = Button(win, text="UPDATE", command=update_data,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b7.place(x=400, y=695)

# ---------- IMPORT / EXPORT LABELS ----------

l9 = Label(win, text="IMPORT DATA", bg="white", fg="black",
           width=20, height=1, bd=5, relief="ridge",
           font=("Merriweather", 14, "bold"))
l9.place(x=725, y=580)

l10 = Label(win, text="EXPORT DATA", bg="white", fg="black",
            width=20, height=1, bd=5, relief="ridge",
            font=("Merriweather", 14, "bold"))
l10.place(x=1225, y=580)

# ---------- IMPORT / EXPORT BUTTONS ----------

b11 = tk.Button(win, text="IMPORT EXCEL FILE", command=import_excel,
                relief="ridge", bg="#00E5FF", fg="black", bd=4,
                font=("times new roman", 12, "bold"), width=20)
b11.place(x=750, y=640)

b12 = tk.Button(win, text="IMPORT CSV FILE", command=import_csv,
                relief="ridge", bg="#00E5FF", fg="black", bd=4,
                font=("times new roman", 12, "bold"), width=20)
b12.place(x=750, y=700)

b13 = tk.Button(win, text="EXPORT EXCEL FILE", command=export_excel,
                relief="ridge", bg="#00E5FF", fg="black", bd=4,
                font=("times new roman", 12, "bold"), width=20)
b13.place(x=1250, y=640)

b14 = tk.Button(win, text="EXPORT CSV FILE", command=export_csv,
                relief="ridge", bg="#00E5FF", fg="black", bd=4,
                font=("times new roman", 12, "bold"), width=20)
b14.place(x=1250, y=700)

# ---------------- TREEVIEW ----------------  #

style = ttk.Style()
style.theme_use("clam")

# ── Treeview body ──
style.configure("mystyle.Treeview",
                background="#F5F5F5",
                foreground="black",
                fieldbackground="#F5F5F5",
                font=('Calibri', 12),
                rowheight=30,
                borderwidth=2,
                relief="solid")

# ── Treeview heading ──
style.configure("mystyle.Treeview.Heading",
                font=('Calibri', 12, 'bold'),
                foreground="white",
                background="#4A4A4A",
                borderwidth=2,
                relief="raised",
                padding=(5, 5))

# ── Heading hover effect ──
style.map("mystyle.Treeview.Heading",
          background=[("active", "#333333")],
          foreground=[("active", "white")])

# ── Row selection color ──
style.map("mystyle.Treeview",
          background=[("selected", "#1E90FF")],
          foreground=[("selected", "white")])

# ── Treeview widget ──
view = ttk.Treeview(win, style="mystyle.Treeview", show="headings")
view.place(x=750, y=100, height=400, width=700)

# ── Columns ──
view["columns"] = ("1", "2", "3", "4", "5")

view.column("1", width=90,  anchor=CENTER, minwidth=70,  stretch=False)
view.column("2", width=160, anchor=CENTER, minwidth=100, stretch=True)
view.column("3", width=130, anchor=CENTER, minwidth=100, stretch=False)
view.column("4", width=130, anchor=CENTER, minwidth=100, stretch=False)
view.column("5", width=110, anchor=CENTER, minwidth=80,  stretch=False)

# ── Headings ──
view.heading("1", text="EMP ID")
view.heading("2", text="NAME")
view.heading("3", text="MOBILE NO.")
view.heading("4", text="DEPARTMENT")
view.heading("5", text="SALARY")

# ── Alternating row colors ──
view.tag_configure("evenrow", background="#FFFFFF")
view.tag_configure("oddrow",  background="#DCE6F1")

# ── Row selection mode ──
view.configure(selectmode="browse")

# ── Visible border frame around Treeview ──
tree_frame = tk.Frame(win, bg="#4A4A4A", bd=2, relief="solid")
tree_frame.place(x=748, y=98, height=404, width=704)
view.lift(tree_frame)

# ── Block column resize and heading click ──


def block_event(event):
    if view.identify_region(event.x, event.y) in ("separator", "heading"):
        return "break"


view.bind("<Button-1>", block_event)

# CLEAR BUTTON
b8 = Button(win, text="CLEAR", command=clear_data,
            relief="ridge", bg="gray", fg="white", bd=4,
            font=("times new roman", 12, "bold"), width=15)
b8.place(x=1030, y=550)

win.state('zoomed')
bg_label.lower()
win.mainloop()

# ---------------- This Is Made By Aditya Bobade ----------------  #
# All Rights Reserved
