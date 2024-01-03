import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class BaseApp:
    def __init__(self, root):
        self.root = root

    def setup_gui(self):
        tk.Label(
            self.root,
            text='A D M I N I S T R A T O R',
            font=('Consolas', 20, 'bold'),
            pady=10
        ).pack()

        tk.Label(
            self.root,
            text='You are the Administrator',
            font=('Consolas', 12, 'italic'),
        ).pack(pady=9)

class AdminApp(BaseApp):
    def __init__(self, root):
        super().__init__(root)
        self.root.geometry('500x430')
        self.setup_gui()

        modify_frame = tk.LabelFrame(self.root, text='Modify', font=('Consolas'), padx=20)
        modify_frame.place(x=50, y=100)

        self.add_update_subjects_button = tk.Button(modify_frame, text="Add/Update subjects", command=self.run_subup)
        self.add_update_subjects_button.pack(padx=5, pady=5)

        self.add_update_faculty_button = tk.Button(modify_frame, text="Add/Update Faculty", command=self.open_faculty_window)
        self.add_update_faculty_button.pack(padx=5, pady=5)

        self.assign_subjects_button1 = tk.Button(modify_frame, text="Assign Subjects", command=self.run_sub)
        self.assign_subjects_button1.pack(padx=5, pady=5)

        tt_frame = tk.LabelFrame(text='Timetable', font=('Consolas'), padx=20)
        tt_frame.place(x=250, y=100)

        self.view_timetable_button = tk.Button(tt_frame, text="Timetable", command=self.run_tt)
        self.view_timetable_button.pack(padx=5, pady=5)

        self.view_todolist_button = tk.Button(tt_frame, text="Todolist", command=self.run_td)
        self.view_todolist_button.pack(padx=5, pady=5)

    def run_sub(self):
        os.system('pythonw sub.py')

    def run_tt(self):
        os.system('pythonw schedule.py')

    def run_td(self):
        os.system('pythonw todolist.py')

    def run_subup(self):
        os.system('pythonw addoupsub.py')

    def fetch_faculty(self):
        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def open_faculty_window(self):
        self.faculty_window = tk.Toplevel(self.root)
        self.faculty_window.title("Add/Update Faculty")

        faculty_frame = tk.Frame(self.faculty_window)
        faculty_frame.pack(padx=10, pady=10)

        faculty_listbox = tk.Listbox(faculty_frame, width=30)
        faculty_listbox.pack(side=tk.LEFT, fill=tk.Y)

        faculty_data = self.fetch_faculty()
        for row in faculty_data:
            faculty_listbox.insert(tk.END, row[1])

        faculty_listbox.bind('<<ListboxSelect>>', self.on_faculty_select)

        form_frame = tk.Frame(faculty_frame)
        form_frame.pack(side=tk.RIGHT)

        self.faculty_id_entry = tk.Entry(form_frame)
        self.faculty_name_entry = tk.Entry(form_frame)
        self.password_entry = tk.Entry(form_frame, show="*")

        faculty_id_label = tk.Label(form_frame, text="Faculty ID:")
        faculty_id_label.pack()
        self.faculty_id_entry.pack(pady=5)

        faculty_name_label = tk.Label(form_frame, text="Faculty Name:")
        faculty_name_label.pack()
        self.faculty_name_entry.pack(pady=5)

        password_label = tk.Label(form_frame, text="Password:")
        password_label.pack()
        self.password_entry.pack(pady=5)

        submit_button = tk.Button(form_frame, text="Submit", command=self.submit_faculty)
        submit_button.pack(pady=10)

    def on_faculty_select(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        faculty_data = self.fetch_faculty()
        selected_faculty = faculty_data[index]
        self.faculty_id_entry.delete(0, tk.END)
        self.faculty_id_entry.insert(tk.END, selected_faculty[0])
        self.faculty_name_entry.delete(0, tk.END)
        self.faculty_name_entry.insert(tk.END, selected_faculty[1])
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(tk.END, selected_faculty[2])

    def submit_faculty(self):
        faculty_id = self.faculty_id_entry.get()
        faculty_name = self.faculty_name_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM faculty WHERE faculty_id=?', (faculty_id,))
        data = cursor.fetchone()

        if data:
            cursor.execute('UPDATE faculty SET faculty_name=?, password=? WHERE faculty_id=?', (faculty_name, password, faculty_id))
            messagebox.showinfo("Success", "Faculty information updated successfully")
        else:
            cursor.execute('INSERT INTO faculty (faculty_id, faculty_name, password) VALUES (?, ?, ?)', (faculty_id, faculty_name, password))
            messagebox.showinfo("Success", "Faculty added successfully")

        conn.commit()
        conn.close()
        self.faculty_window.destroy()

ad = tk.Tk()
app = AdminApp(ad)
ad.mainloop()
