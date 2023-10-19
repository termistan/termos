from base64 import b16decode, b16encode
from stringprep import b1_set
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class Termapp:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="black")
        self.master = master
        self.master.title("sputnik 1500s")

        self.conn = sqlite3.connect('winlin.db')
        self.create_table()

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                salary INTEGER
            )
        ''')
        
        
    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="Add User", command=self.add_employee, width=15, bg="green", fg="white", font=("Arial", 14))
        self.add_button.pack(pady=5)
        self.update_button = tk.Button(self.master, text="Update User", command=self.update_employee, width=15, bg="blue", fg="white", font=("Arial", 14))
        self.update_button.pack(pady=5)
        self.delete_button = tk.Button(self.master, text="Delete User", command=self.delete_employee, width=15, bg="violet", fg="white", font=("Arial", 14))
        self.delete_button.pack(pady=5)
        self.search_button = tk.Button(self.master, text="Search User", command=self.search_employee, width=15, bg="yellow", fg="white", font=("Arial", 14))
        self.search_button.pack(pady=5)
        self.undo_button = tk.Button(self.master, text="Undo", command=self.undo_action, width=15, bg="turquoise", fg="grey", font=("Arial", 14))
        self.undo_button.pack(pady=5)


        # Bind double click event on treeview
        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None  # To store the last action for undo

    def add_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")
        email = simpledialog.askstring("Input", "Enter employee email:")
        phone = simpledialog.askstring("Input", "Enter employee phone:")
        salary = simpledialog.askinteger("Input", "Enter employee salary:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "add"

    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Input", "Enter updated employee name:", initialvalue=employee[1])
            phone = simpledialog.askstring("Input", "Enter updated employee phone:", initialvalue=employee[2])
            email = simpledialog.askstring("Input", "Enter updated employee email:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Input", "Enter updated employee salary:", initialvalue=employee[4])

            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = "update"
        else:
            messagebox.showerror("Error", "Employee not found.")

    def delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "delete"

    def search_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", "No employee found with the given name.")

    def update_treeview(self):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        for employee in employees:
            self.tree.insert("", "end", values=employee)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee_id = self.tree.item(item, "values")[0]  # Get the employee ID
        messagebox.showinfo("Employee ID", f"Employee ID: {employee_id}")

    def undo_action(self):
        if self.last_action == "add":
            messagebox.showinfo("Undo", "Undo Add Employee action")
            # Implement code to undo the add action
        elif self.last_action == "update":
            messagebox.showinfo("Undo", "Undo Update Employee action")
            # Implement code to undo the update action
        elif self.last_action == "delete":
            messagebox.showinfo("Undo", "Undo Delete Employee action")
            # Implement code to undo the delete action
        else:
            messagebox.showinfo("Undo", "No previous action to undo")

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Termapp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()