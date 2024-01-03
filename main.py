import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import timetable_fac
import sqlite3
import os
from abc import ABC, abstractmethod

class TimetableApp(ABC):
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x430')
        self.root.title('Welcome')

    @abstractmethod
    def create_widgets(self):
        pass

    def show_password(self):
        if self.passw_entry['show'] == "●":
            self.passw_entry['show'] = ""
            self.B1_show['text'] = '●'
        else:
            self.passw_entry['show'] = "●"
            self.B1_show['text'] = '○'

    @abstractmethod
    def challenge(self):
        pass

class TimetableAppImplementation(TimetableApp):
    def create_widgets(self):
        tk.Label(
            self.root,
            text='TIMETABLE MANAGEMENT SYSTEM',
            font=('Consolas', 20, 'bold'),
            wrap=400
        ).pack(pady=20)

        tk.Label(
            self.root,
            text='Username',
            font=('Consolas', 15)
        ).pack()

        self.id_entry = tk.Entry(
            self.root,
            font=('Consolas', 12),
            width=21
        )
        self.id_entry.pack()

        tk.Label(
            self.root,
            text='Password:',
            font=('Consolas', 15)
        ).pack()

        self.passw_entry = tk.Entry(
            self.root,
            font=('Consolas', 12),
            width=15,
            show="●"
        )
        self.passw_entry.pack()

        self.B1_show = tk.Button(
            self.root,
            text='○',
            font=('Consolas', 12, 'bold'),
            command=self.show_password,
            padx=5
        )
        self.B1_show.pack(padx=15)

        self.combo1 = ttk.Combobox(
            self.root,
            values=['Faculty', 'Admin']
        )
        self.combo1.pack(pady=15)
        self.combo1.current(1)

        tk.Button(
            self.root,
            text='Login',
            font=('Consolas', 12, 'bold'),
            padx=30,
            command=self.challenge
        ).pack(pady=10)

    def challenge(self):
        conn = sqlite3.connect(r'timetable.db')
        user = str(self.combo1.get())

        if user == "Faculty":
            cursor = conn.execute(f"SELECT password, faculty_id FROM FACULTY WHERE faculty_id='{self.id_entry.get()}'")
            cursor = list(cursor)
            if len(cursor) == 0:
                messagebox.showwarning('Bad id', 'No such user found!')
            elif self.passw_entry.get() != cursor[0][0]:
                messagebox.showerror('Bad pass', 'Incorrect Password!')
            else:
                self.root.destroy()
                # Call the faculty timetable function with the faculty ID
                timetable_fac.fac_tt_frame(cursor[0][1])

        elif user == "Admin":
            if self.id_entry.get() == 'sridevi' and self.passw_entry.get() == 'asdf@123':
                self.root.destroy()
                os.system('python adminpg.py')
            else:
                messagebox.showerror('Bad Input', 'Incorrect Username/Password')

root = tk.Tk()
app = TimetableAppImplementation(root)
app.create_widgets()
root.mainloop()