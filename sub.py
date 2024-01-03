import tkinter as tk
from tkinter import messagebox
import sqlite3

class DatabaseManager:
    def __init__(self, db_name='timetable.db'):
        self.db_name = db_name

    def execute_query(self, query, parameters=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    def execute_update(self, query, parameters):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        conn.close()

class FacultyManager(DatabaseManager):
    def add_subject_to_faculty(self, faculty_name, subject_name):
        faculty_id = self.get_faculty_id(faculty_name)
        subject_info = f"{subject_name} ({self.get_subject_code(subject_name)})"
        self.execute_update("UPDATE faculty SET subject = ? WHERE faculty_id = ?", (subject_info, faculty_id))
        self.execute_update("INSERT INTO faculty_subjects (faculty_name, subject_name, faculty_id) VALUES (?, ?, ?)", (faculty_name, subject_name, faculty_id))

    def get_faculty_id(self, faculty_name):
        result = self.execute_query("SELECT faculty_id FROM faculty WHERE faculty_name=?", (faculty_name,))
        if result:
            return result[0][0]
        return None

    def get_subject_code(self, subject_name):
        result = self.execute_query("SELECT code FROM subjects WHERE name=?", (subject_name,))
        if result:
            return result[0][0]
        return None

class SubjectManager(DatabaseManager):
    def get_subject_names(self):
        result = self.execute_query("SELECT name FROM subjects")
        return [row[0] for row in result]

class AssignmentGUI(FacultyManager,SubjectManager):
    def __init__(self, root, faculty_manager, subject_manager):
        self.root = root
        self.faculty_manager = faculty_manager
        self.subject_manager = subject_manager

        self.setup_ui()

    def save_assignment(self, selected_faculty, selected_subject):
        faculty_name = selected_faculty.get()
        subject_name = selected_subject.get()

        if faculty_name and subject_name:
            self.faculty_manager.add_subject_to_faculty(faculty_name, subject_name)
            messagebox.showinfo("Success", f"{subject_name} assigned to {faculty_name} successfully")
        else:
            messagebox.showerror("Error", "No faculty or subject found")

    def setup_ui(self):
        assign_frame = tk.Frame(self.root)
        assign_frame.pack(padx=10, pady=10)

        faculty_names = self.faculty_manager.execute_query("SELECT faculty_name FROM faculty")
        faculty_names = [row[0] for row in faculty_names]
        selected_faculty = tk.StringVar(self.root)
        selected_faculty.set(faculty_names[0])
        faculty_dropdown = tk.OptionMenu(assign_frame, selected_faculty, *faculty_names)
        faculty_dropdown.pack(pady=5)

        subject_names = self.subject_manager.get_subject_names()
        selected_subject = tk.StringVar(self.root)
        selected_subject.set(subject_names[0])
        subjects_dropdown = tk.OptionMenu(assign_frame, selected_subject, *subject_names)
        subjects_dropdown.pack(pady=5)

        assign_button = tk.Button(assign_frame, text="Assign", command=lambda: self.save_assignment(selected_faculty, selected_subject))
        assign_button.pack(pady=10)

def main():
    root = tk.Tk()
    root.title("Administrator Panel")

    faculty_manager = FacultyManager()
    subject_manager = SubjectManager()

    assignment_gui = AssignmentGUI(root, faculty_manager, subject_manager)

    root.mainloop()


main()
