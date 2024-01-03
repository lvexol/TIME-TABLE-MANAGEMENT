import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
import sqlite3

def update_todo_function(faculty_id):
    def save_task():
        task = task_entry.get()
        start_date = start_date_entry.get_date()  # Get the selected starting date
        end_date = end_date_entry.get_date()  # Get the selected ending date
        start_date_str = start_date.strftime("%Y-%m-%d")  # Convert date to string
        end_date_str = end_date.strftime("%Y-%m-%d")  # Convert date to string

        # Save the task data into your database table
        conn = sqlite3.connect(r'timetable.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO task (faculty_id, task, start_date, end_date) VALUES (?, ?, ?, ?)",
                       (faculty_id, task, start_date_str, end_date_str))
        conn.commit()
        conn.close()
        messagebox.showinfo('Task Saved', 'Task has been saved successfully!')
        # Close the current window and open the tasks window
        nw.destroy()
        view_tasks(faculty_id)

    def view_tasks(faculty_id):
        tasks_window = tk.Tk()
        tasks_window.title('View Tasks')
        tk.Label(
            tasks_window,
            text='Your Tasks:',
            font=('Consolas', 15)
        ).pack()

        # Query tasks for the faculty
        conn = sqlite3.connect(r'timetable.db')
        cursor = conn.cursor()
        cursor.execute("SELECT task, start_date, end_date FROM task WHERE faculty_id = ?", (faculty_id,))
        tasks = cursor.fetchall()
        conn.close()

        for task in tasks:
            task_str = f"Task: {task[0]}\nStart Date: {task[1]}\nEnd Date: {task[2]}\n"
            tk.Label(
                tasks_window,
                text=task_str,
                font=('Consolas', 12)
            ).pack()

        tasks_window.mainloop()

    nw = tk.Tk()
    nw.title('Update To-Do')
    tk.Label(
        nw,
        text='Enter Task:',
        font=('Consolas', 15)
    ).pack()
    task_entry = tk.Entry(
        nw,
        font=('Consolas', 12),
        width=21
    )
    task_entry.pack()

    tk.Label(
        nw,
        text='Start Date:',
        font=('Consolas', 15)
    ).pack()
    start_date_entry = DateEntry(
        nw,
        font=('Consolas', 12),
        width=21,
        date_pattern="yyyy-mm-dd"
    )
    start_date_entry.pack()

    tk.Label(
        nw,
        text='End Date:',
        font=('Consolas', 15)
    ).pack()
    end_date_entry = DateEntry(
        nw,
        font=('Consolas', 12),
        width=21,
        date_pattern="yyyy-mm-dd"
    )
    end_date_entry.pack()

    save_button = tk.Button(
        nw,
        text="Save Task",
        font=('Consolas', 12, 'bold'),
        padx=30,
        command=save_task
    )
    save_button.pack(pady=10)

    view_button = tk.Button(
        nw,
        text="View Tasks",
        font=('Consolas', 12, 'bold'),
        padx=30,
        command=lambda: view_tasks(faculty_id)
    )
    view_button.pack(pady=10)

    nw.mainloop()



def create_tasks_table():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY,
            faculty_id TEXT,
            task TEXT,
            start_date TEXT,
            end_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fac_tt_frame(facid):
    root = tk.Tk()
    root.title(f"Faculty Schedule - ID: {facid}")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    periods = list(range(1, 8))  # Periods range from 1 to 7

    schedule_frame = tk.Frame(root)
    schedule_frame.pack()

    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    buttons = {}
    for j, period in enumerate(periods):
        label = tk.Label(schedule_frame, text=f"Hour {period}", width=15, borderwidth=1, relief="solid")
        label.grid(row=0, column=j + 1)

    for i, day in enumerate(days, start=1):
        label = tk.Label(schedule_frame, text=day, width=15, borderwidth=1, relief="solid")
        label.grid(row=i, column=0)

        for j, period in enumerate(periods, start=1):
            cursor.execute("SELECT SUBCODE FROM hours WHERE DAYID = ? AND PERIODID = ? AND FACID = ?", (i, j, facid))
            data = cursor.fetchone()

            button_text = data[0] if data else "No Subject"
            button = tk.Button(schedule_frame, text=button_text, width=15, height=2)
            button.grid(row=i, column=j)
            buttons[(day, j)] = button

            button.config(command=lambda day=i, period=j, button=button: update_todo_function(facid))

    root.mainloop()
