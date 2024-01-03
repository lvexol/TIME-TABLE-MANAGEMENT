import tkinter as tk
from tkinter import messagebox
import sqlite3

class SubjectManagementApp:
    def __init__(self):
        self.count = 1
        self.top = None
        self.faculty_dropdown = None
        self.submit_button = None

        self.root = tk.Tk()
        self.root.title("Administrator Panel")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.add_update_subject_button = tk.Button(self.frame, text="Add/View Subjects", command=self.open_subject_window)
        self.add_update_subject_button.pack(padx=5, pady=5)

    def insert_subject(self, name, code):
        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO subjects (name, code) VALUES (?, ?)', (name, code))
        conn.commit()
        conn.close()

    def submit_subject(self, name_entry, code_entry):
        name = name_entry.get()
        code = code_entry.get()
        self.insert_subject(name, code)
        messagebox.showinfo("Success", "Subject added/updated successfully")
        self.top.destroy()

    def update_subject(self, name_entry, code_entry, faculty_variable):
        subject_name = name_entry.get()
        subject_code = code_entry.get()
        assigned_faculty = faculty_variable.get()

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE faculty_subjects SET faculty_name=? WHERE subject_name=?", (assigned_faculty, subject_name))
        conn.commit()
        conn.close()

    def on_subject_select(self, event, name_entry, code_entry, faculty_entry):
        assigned_faculty = None
        w = event.widget
        index = int(w.curselection()[0])
        selected_subject = w.get(index)

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, code FROM subjects WHERE name=?", (selected_subject,))
        subject_data = cursor.fetchone()
        conn.close()

        if subject_data:
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, subject_data[0])
            code_entry.delete(0, tk.END)
            code_entry.insert(tk.END, subject_data[1])

            if self.count == 0:
                self.submit_button.destroy()

            conn = sqlite3.connect('timetable.db')
            cursor = conn.cursor()
            cursor.execute("SELECT faculty_name FROM faculty_subjects WHERE subject_name=?", (selected_subject,))
            assigned_faculty = cursor.fetchone()
            conn.close()

            if assigned_faculty is not None:
                faculty_entry.config(state='normal')
                faculty_entry.delete(0, tk.END)
                faculty_entry.insert(0, assigned_faculty[0])
                faculty_entry.config(state='readonly')
            else:
                faculty_entry.config(state='normal')
                faculty_entry.delete(0, tk.END)
                faculty_entry.insert(0, "Unassigned")
                faculty_entry.config(state='readonly')

    def open_subject_window(self):
        self.faculty_dropdown = None
        self.count = 0

        self.top = tk.Toplevel(self.root)
        self.top.title("Add/Update Subject")

        subject_frame = tk.Frame(self.top)
        subject_frame.pack(padx=10, pady=10)

        subject_listbox = tk.Listbox(subject_frame, width=30)
        subject_listbox.grid(row=0, column=0, padx=5, pady=5, rowspan=3)

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()

        for row in subjects:
            subject_listbox.insert(tk.END, row)

        form_frame = tk.Frame(subject_frame)
        form_frame.grid(row=0, column=1, padx=10, pady=10)

        name_label = tk.Label(form_frame, text="Subject Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        code_label = tk.Label(form_frame, text="Subject Code:")
        code_label.grid(row=1, column=0, padx=5, pady=5)
        code_entry = tk.Entry(form_frame)
        code_entry.grid(row=1, column=1, padx=5, pady=5)

        faculty_label = tk.Label(form_frame, text="Faculty:")
        faculty_label.grid(row=2, column=0, padx=5, pady=5)
        faculty_entry = tk.Entry(form_frame, state='readonly')
        faculty_entry.insert(0, "Unassigned")
        faculty_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(form_frame, text="Submit", command=lambda: self.submit_subject(name_entry, code_entry))
        self.submit_button.grid(row=3, column=1, padx=5, pady=10)

        subject_listbox.bind('<<ListboxSelect>>', lambda event: self.on_subject_select(event, name_entry, code_entry, faculty_entry))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SubjectManagementApp()
    app.run()
