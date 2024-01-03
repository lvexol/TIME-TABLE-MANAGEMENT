import tkinter as tk
from tkinter import messagebox
import sqlite3

class SchoolScheduleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Schedule")

        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.periods = list(range(1, 8))  # Periods range from 1 to 7

        self.schedule_frame = tk.Frame(self.root)
        self.schedule_frame.pack()

        self.selected_class = 1  # Default class ID is set to 1
        self.buttons = {}
        self.selected_class_var = tk.StringVar()  # Define selected_class_var as an instance variable

        self.setup_gui()

    def select_subject(self, day, period, button):
        def subject_selection():
            selected_subject = self.subject_var.get()
            messagebox.showinfo("Selected Subject", f"You selected: {selected_subject}")
            button.config(text=selected_subject)

            
            conn = sqlite3.connect('timetable.db')
            cursor = conn.cursor()
            cursor.execute("SELECT faculty_id FROM faculty_subjects WHERE subject_name = ?", (selected_subject,))
            faculty_id = cursor.fetchone()
            if faculty_id:
                faculty_id = faculty_id[0]
            
            update_query = f"UPDATE hours SET SUBCODE = ?,facid = ? WHERE DAYID = ? AND PERIODID = ? AND ID = ?"
            cursor.execute(update_query, (selected_subject,faculty_id, day, period, self.selected_class))
            conn.commit()
            conn.close()

            popup.destroy()

        popup = tk.Toplevel()
        popup.title(f"Select Subject for Day {day} - Period {period}")

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT name FROM subjects")
        subject = [row[0] for row in cursor.fetchall()]

        self.subject_var = tk.StringVar(popup)
        self.subject_var.set("Select Subject")

        if not subject:
            subject = ["No Subject"]

        subject_menu = tk.OptionMenu(popup, self.subject_var, *subject)
        subject_menu.pack()

        select_button = tk.Button(popup, text="Select", command=subject_selection, width=10)
        select_button.pack()

    def setup_gui(self):
        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()

        for j, period in enumerate(self.periods):
            label = tk.Label(self.schedule_frame, text=f"Hour {period}", width=15, borderwidth=1, relief="solid")
            label.grid(row=0, column=j + 1)

        for i, day in enumerate(self.days, start=1):
            label = tk.Label(self.schedule_frame, text=day, width=15, borderwidth=1, relief="solid")
            label.grid(row=i, column=0)

            for j, period in enumerate(self.periods, start=1):
                cursor.execute("SELECT SUBCODE FROM hours WHERE DAYID = ? AND PERIODID = ? AND ID = ?", (i, j, self.selected_class))
                data = cursor.fetchone()

                button_text = data[0] if data else "No Subject"
                button = tk.Button(self.schedule_frame, text=button_text, width=15, height=2)
                button.grid(row=i, column=j)
                self.buttons[(day, j)] = button

                button.config(command=lambda day=i, period=j, button=button: self.select_subject(day, period, button))

        self.selected_class_var.set(str(self.selected_class))  # Set the value for selected_class_var

        option_menu = tk.OptionMenu(self.schedule_frame, self.selected_class_var, "1", "2", "3", "4")
        option_menu.grid(row=len(self.days) + 2, column=3, columnspan=4, padx=10, pady=10)

        set_button = tk.Button(self.schedule_frame, text="Set Class ID", command=self.set_selected_class)
        set_button.grid(row=len(self.days) + 3, column=3, columnspan=4, padx=10, pady=10)

        conn.close()

    def set_selected_class(self):
        self.selected_class = int(self.selected_class_var.get())
        self.setup_gui()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SchoolScheduleApp()
    app.run()