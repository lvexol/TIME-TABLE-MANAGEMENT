import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

# Create a database
conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

# Create a table to store faculty details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faculty (
        faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_name TEXT
    )
''')

# Create a table to store tasks for faculties
cursor.execute('''
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        task TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
    )
''')

conn.commit()

def add_task():
    selected_faculty_id = faculty_id_var.get()
    task = task_entry.get()
    start_date = start_date_picker.get()
    end_date = end_date_picker.get()
    
    cursor.execute("INSERT INTO task (faculty_id, task, start_date, end_date) VALUES (?, ?, ?, ?)", (selected_faculty_id, task, start_date, end_date))
    conn.commit()
    
    load_tasks_for_faculty(selected_faculty_id)

def delete_task():
    selected_faculty_id = faculty_id_var.get()
    selected_item = table_dict[selected_faculty_id].selection()
    
    if selected_item:
        item_id = table_dict[selected_faculty_id].item(selected_item)['values'][0]
        
        cursor.execute("DELETE FROM task WHERE id = ?", (item_id,))
        conn.commit()
        
        load_tasks_for_faculty(selected_faculty_id)
        table_dict[selected_faculty_id].delete(selected_item)

def view_tasks():
    selected_faculty_id = faculty_id_var.get()
    load_tasks_for_faculty(selected_faculty_id)
    table_frame.pack()

def clear_table(faculty_id):
    for item in table_dict[faculty_id].get_children():
        table_dict[faculty_id].delete(item)

def load_tasks_for_faculty(selected_faculty_id):
    if selected_faculty_id != "No Faculty IDs Found":
        clear_table(selected_faculty_id)
    
        cursor.execute("SELECT id, task, start_date, end_date FROM task WHERE faculty_id = ?", (selected_faculty_id,))
        for row in cursor.fetchall():
            table_dict[selected_faculty_id].insert('', 'end', values=row)

def show_faculty_widgets(event):
    selected_faculty_id = faculty_id_var.get()
    for faculty_id, table in table_dict.items():
        if faculty_id == selected_faculty_id:
            table.grid()
        else:
            table.grid_remove()

root = tk.Tk()
root.title("Faculty To-Do List")

# Create a dropdown for selecting faculty IDs from the "faculty" table
faculty_frame = ttk.Frame(root)
faculty_frame.pack(pady=10)
faculty_label = ttk.Label(faculty_frame, text="Select Faculty:")
faculty_label.grid(row=0, column=0, padx=5)

cursor.execute("SELECT faculty_id, faculty_name FROM faculty")
faculty_data = cursor.fetchall()
faculty_ids = [row[0] for row in faculty_data]
faculty_names = [row[1] for row in faculty_data]

faculty_id_var = tk.StringVar()

if faculty_ids:
    faculty_id_var.set(faculty_ids[0])
else:
    faculty_ids = ["No Faculty IDs Found"]

faculty_dropdown = ttk.Combobox(faculty_frame, textvariable=faculty_id_var, values=faculty_ids)
faculty_dropdown.grid(row=0, column=1)
faculty_dropdown.bind("<<ComboboxSelected>>", show_faculty_widgets)

# Create tables and entry fields
table_dict = {}
entry_frame = ttk.Frame(root)
entry_frame.pack(pady=10)

task_label = ttk.Label(entry_frame, text="Task:")
task_label.grid(row=0, column=0)
task_entry = ttk.Entry(entry_frame, width=40)
task_entry.grid(row=0, column=1)

start_date_label = ttk.Label(entry_frame, text="Start Date:")
start_date_label.grid(row=0, column=2)
start_date_picker = DateEntry(entry_frame, width=12)
start_date_picker.grid(row=0, column=3)

end_date_label = ttk.Label(entry_frame, text="End Date:")
end_date_label.grid(row=0, column=4)
end_date_picker = DateEntry(entry_frame, width=12)
end_date_picker.grid(row=0, column=5)

add_button = ttk.Button(entry_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=6)

delete_button = ttk.Button(entry_frame, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=7)

view_button = ttk.Button(entry_frame, text="View Tasks", command=view_tasks)
view_button.grid(row=0, column=8)

# Create the table frame
table_frame = ttk.Frame(root)

for faculty_id in faculty_ids:
    columns = ("ID", "Task", "Start Date", "End Date")
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
        if col == "Task":
            table.column(col, width=300)
        else:
            table.column(col, width=100)
    table.grid(row=0, column=0)
    table_dict[faculty_id] = table
    table.grid_remove()

root.mainloop()

conn.close()
