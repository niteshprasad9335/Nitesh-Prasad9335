import os
import sqlite3
import hashlib
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk
from PIL import Image


# ============================================================
# SETTINGS
# ============================================================

DB_NAME = "hospital.db"
HOSPITAL_IMAGE ="D:\\Movie\\240_F_887484150_JZ9SOJ5uO5lQHImxXTXC8fbgVIfFHnep.jpg"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ============================================================
# COLORS
# ============================================================

BG = "#579CE0"
SIDEBAR = "#0B5ED7"
SIDEBAR_DARK = "#084298"

BLUE = "#0D6EFD"
CYAN = "#0DCaf0"
GREEN = "#198754"
ORANGE = "#FD7E14"
RED = "#73D4BC"
PURPLE = "#6F42C1"

WHITE = "#F0F3F2"
TEXT = "#172B4D"
MUTED = "#6C757D"


# ============================================================
# DATABASE
# ============================================================

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_database():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            qualification TEXT,
            department TEXT,
            mobile TEXT,
            available_time TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            mobile TEXT,
            address TEXT,
            blood_group TEXT,
            disease TEXT,
            admission_date TEXT,
            doctor_id INTEGER,
            FOREIGN KEY(doctor_id)
            REFERENCES doctors(id)
            ON DELETE SET NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date TEXT,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Booked',
            FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE CASCADE,
            FOREIGN KEY(doctor_id)
            REFERENCES doctors(id)
            ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0,
            expiry_date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_fee REAL DEFAULT 0,
            medicine_charges REAL DEFAULT 0,
            room_charges REAL DEFAULT 0,
            other_charges REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            payment_status TEXT DEFAULT 'Pending',
            bill_date TEXT,
            FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE SET NULL
        )
    """)

    cur.execute(
        "SELECT id FROM users WHERE username=?",
        ("admin",)
    )

    if cur.fetchone() is None:

        cur.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            ("admin", password_hash("admin123"))
        )

    conn.commit()
    conn.close()


# ============================================================
# APP
# ============================================================

class HospitalApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Hospital Management System"
        )

        self.root.geometry("1400x800")
        self.root.minsize(1100, 850)

        self.current_page = None

        self.show_login()

    # ========================================================
    # LOGIN
    # ========================================================

    def show_login(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(fg_color=BG)

        main = ctk.CTkFrame(
            self.root,
            fg_color=BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        # LEFT IMAGE

        left = ctk.CTkFrame(
            main,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        left.pack(
            side="left",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            left,
            text="🏥",
            font=("Arial", 70)
        ).pack(pady=(70, 50))

        ctk.CTkLabel(
            left,
            text="HOSPITAL",
            font=("Arial", 36, "bold"),
            text_color=WHITE
        ).pack()

        ctk.CTkLabel(
            left,
            text="MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            text_color="#809EC7"
        ).pack(pady=5)

        ctk.CTkLabel(
            left,
            text="Smart • Secure • Simple",
            font=("Arial", 16),
            text_color="#7B6DB9"
        ).pack(pady=20)

        if os.path.exists(HOSPITAL_IMAGE):

            try:

                image = Image.open(
                    HOSPITAL_IMAGE
                )

                image.thumbnail((600, 300))

                self.login_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(600, 300)
                )

                ctk.CTkLabel(
                    left,
                    text="",
                    image=self.login_image
                ).pack(pady=20)

            except:
                pass

        else:

            ctk.CTkLabel(
                left,
                text="Hospital Photo\n\n"
                     "Add hospital.jpg\n"
                     "to the project folder",
                font=("Arial", 18),
                text_color="#B1B147"
            ).pack(pady=40)

        # RIGHT LOGIN

        right = ctk.CTkFrame(
            main,
            fg_color=WHITE,
            corner_radius=0
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        box = ctk.CTkFrame(
            right,
            fg_color=WHITE,
            width=420
        )

        box.place(
            relx=.5,
            rely=.5,
            anchor="center"
        )

        ctk.CTkLabel(
            box,
            text="Welcome Back 👋",
            font=("Arial", 30, "bold"),
            text_color=TEXT
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            box,
            text="Login to Hospital Management System",
            font=("Arial", 14),
            text_color=MUTED
        ).pack(pady=(0, 30))

        ctk.CTkLabel(
            box,
            text="Username",
            font=("Arial", 14, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        self.username = ctk.CTkEntry(
            box,
            width=380,
            height=45,
            placeholder_text="Enter username"
        )

        self.username.pack(pady=(5, 18))

        ctk.CTkLabel(
            box,
            text="Password",
            font=("Arial", 14, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        self.password = ctk.CTkEntry(
            box,
            width=380,
            height=45,
            placeholder_text="Enter password",
            show="*"
        )

        self.password.pack(pady=(5, 25))

        ctk.CTkButton(
            box,
            text="LOGIN",
            width=380,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color=BLUE,
            hover_color=SIDEBAR_DARK,
            command=self.login
        ).pack()

        ctk.CTkLabel(
            box,
            text="Default: admin / admin123",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(pady=20)

    # ========================================================
    # LOGIN CHECK
    # ========================================================

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        if not username or not password:

            messagebox.showwarning(
                "Login",
                "Username and password required."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id FROM users
            WHERE username=? AND password=?
            """,
            (
                username,
                password_hash(password)
            )
        )

        user = cur.fetchone()

        conn.close()

        if user:

            self.show_main()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    # ========================================================
    # MAIN WINDOW
    # ========================================================

    def show_main(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        # SIDEBAR

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=240,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="🏥",
            font=("Arial", 42)
        ).pack(pady=(25, 0))

        ctk.CTkLabel(
            self.sidebar,
            text="HOSPITAL",
            font=("Arial", 22, "bold"),
            text_color=WHITE
        ).pack()

        ctk.CTkLabel(
            self.sidebar,
            text="MANAGEMENT",
            font=("Arial", 12),
            text_color="#DCEBFF"
        ).pack(pady=(0, 25))

        menu = [
            ("🏠  Dashboard", self.dashboard),
            ("👤  Patients", self.patient_module),
            ("👨‍⚕️  Doctors", self.doctor_module),
            ("📅  Appointments", self.appointment_module),
            ("💊  Medicines", self.medicine_module),
            ("🧾  Billing", self.billing_module)
        ]

        for text, command in menu:

            ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color=SIDEBAR_DARK,
                text_color=WHITE,
                font=("Arial", 14, "bold"),
                command=command
            ).pack(
                fill="x",
                padx=12,
                pady=3
            )

        ctk.CTkButton(
            self.sidebar,
            text="🚪  Logout",
            height=45,
            fg_color=RED,
            hover_color="#A71D2A",
            font=("Arial", 14, "bold"),
            command=self.show_login
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        # CONTENT

        self.content = ctk.CTkFrame(
            self.root,
            fg_color=BG,
            corner_radius=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.dashboard()

    # ========================================================
    # HEADER
    # ========================================================

    def page_header(self, title, subtitle=""):

        header = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            height=85,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).pack(
            side="left",
            padx=25
        )

        if subtitle:

            ctk.CTkLabel(
                header,
                text=subtitle,
                font=("Arial", 13),
                text_color=MUTED
            ).pack(
                side="right",
                padx=25
            )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def dashboard(self):

        self.clear_content()

        self.page_header(
            "Dashboard",
            f"Today: {date.today()}"
        )

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM patients"
        )
        patients = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM doctors"
        )
        doctors = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*) FROM appointments
            WHERE appointment_date=?
            """,
            (str(date.today()),)
        )

        appointments = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM medicines"
        )
        medicines = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM bills"
        )
        bills = cur.fetchone()[0]

        conn.close()

        cards = [
            ("👤", "Total Patients", patients, BLUE),
            ("👨‍⚕️", "Total Doctors", doctors, GREEN),
            ("📅", "Today's Appointments", appointments, ORANGE),
            ("💊", "Total Medicines", medicines, PURPLE),
            ("🧾", "Total Bills", bills, RED)
        ]

        grid = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        grid.pack(
            fill="x",
            padx=25,
            pady=25
        )

        for i, (icon, text, value, color) in enumerate(cards):

            card = ctk.CTkFrame(
                grid,
                fg_color=WHITE,
                corner_radius=15
            )

            card.grid(
                row=0,
                column=i,
                padx=7,
                sticky="nsew"
            )

            grid.grid_columnconfigure(
                i,
                weight=1
            )

            ctk.CTkLabel(
                card,
                text=icon,
                font=("Arial", 30)
            ).pack(
                pady=(18, 5)
            )

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 28, "bold"),
                text_color=color
            ).pack()

            ctk.CTkLabel(
                card,
                text=text,
                font=("Arial", 12),
                text_color=MUTED
            ).pack(
                pady=(0, 18)
            )

        welcome = ctk.CTkFrame(
            self.content,
            fg_color=SIDEBAR,
            corner_radius=20
        )

        welcome.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        ctk.CTkLabel(
            welcome,
            text="🏥  Welcome to Hospital Management System",
            font=("Arial", 30, "bold"),
            text_color=WHITE
        ).pack(pady=(50, 15))

        ctk.CTkLabel(
            welcome,
            text="Manage Patients • Doctors • Appointments • Medicines • Billing",
            font=("Arial", 16),
            text_color="#68C451"
        ).pack()

    # ========================================================
    # PATIENTS
    # ========================================================

    def patient_module(self):

        self.clear_content()

        self.page_header(
            "Patient Management",
            "Add / Update / Delete / Search"
        )

        form = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=15
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        fields = [
            "Name",
            "Age",
            "Gender",
            "Mobile",
            "Address",
            "Blood Group",
            "Disease",
            "Admission Date",
            "Doctor ID"
        ]

        self.patient_entries = {}

        for i, field in enumerate(fields):

            row = i // 3
            col = (i % 3) * 2

            ctk.CTkLabel(
                form,
                text=field,
                text_color=TEXT,
                font=("Arial", 12, "bold")
            ).grid(
                row=row,
                column=col,
                padx=10,
                pady=(12, 2),
                sticky="w"
            )

            entry = ctk.CTkEntry(
                form,
                width=220,
                height=35
            )

            entry.grid(
                row=row + 1,
                column=col,
                padx=10,
                pady=(0, 12)
            )

            self.patient_entries[field] = entry

        self.patient_entries[
            "Admission Date"
        ].insert(
            0,
            str(date.today())
        )

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack(pady=5)

        self.colored_button(
            buttons,
            "➕ Add",
            GREEN,
            self.add_patient
        )

        self.colored_button(
            buttons,
            "✏ Update",
            BLUE,
            self.update_patient
        )

        self.colored_button(
            buttons,
            "🗑 Delete",
            RED,
            self.delete_patient
        )

        self.colored_button(
            buttons,
            "🔄 Clear",
            ORANGE,
            self.clear_patient
        )

        search = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        search.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.patient_search = ctk.CTkEntry(
            search,
            width=300,
            height=38,
            placeholder_text="Search patient..."
        )

        self.patient_search.pack(
            side="left"
        )

        ctk.CTkButton(
            search,
            text="🔎 Search",
            width=100,
            command=self.search_patients
        ).pack(
            side="left",
            padx=8
        )

        table_frame = tk.Frame(
            self.content,
            bg=WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Name",
            "Age",
            "Gender",
            "Mobile",
            "Blood",
            "Disease",
            "Doctor"
        )

        self.patient_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.patient_tree.heading(
                col,
                text=col
            )

            self.patient_tree.column(
                col,
                width=120
            )

        self.patient_tree.pack(
            fill="both",
            expand=True
        )

        self.patient_tree.bind(
            "<ButtonRelease-1>",
            self.select_patient
        )

        self.load_patients()

    # ========================================================
    # BUTTON HELPER
    # ========================================================

    def colored_button(
        self,
        parent,
        text,
        color,
        command
    ):

        ctk.CTkButton(
            parent,
            text=text,
            width=120,
            height=38,
            fg_color=color,
            hover_color=color,
            command=command
        ).pack(
            side="left",
            padx=5
        )

    # ========================================================
    # PATIENT FUNCTIONS
    # ========================================================

    def get_patient_data(self):

        return {
            key: value.get().strip()
            for key, value in
            self.patient_entries.items()
        }

    def add_patient(self):

        data = self.get_patient_data()

        if not data["Name"]:

            messagebox.showwarning(
                "Validation",
                "Patient name is required."
            )

            return

        try:

            age = (
                int(data["Age"])
                if data["Age"]
                else None
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Age must be a number."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO patients
            (
                name,age,gender,mobile,address,
                blood_group,disease,admission_date,
                doctor_id
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                data["Name"],
                age,
                data["Gender"],
                data["Mobile"],
                data["Address"],
                data["Blood Group"],
                data["Disease"],
                data["Admission Date"],
                data["Doctor ID"] or None
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Patient added successfully."
        )

        self.clear_patient()
        self.load_patients()

    def load_patients(self, search=""):

        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        if search:

            cur.execute(
                """
                SELECT
                p.id,p.name,p.age,p.gender,
                p.mobile,p.blood_group,
                p.disease,
                COALESCE(d.name,'')
                FROM patients p
                LEFT JOIN doctors d
                ON p.doctor_id=d.id
                WHERE p.name LIKE ?
                OR p.mobile LIKE ?
                """,
                (
                    f"%{search}%",
                    f"%{search}%"
                )
            )

        else:

            cur.execute(
                """
                SELECT
                p.id,p.name,p.age,p.gender,
                p.mobile,p.blood_group,
                p.disease,
                COALESCE(d.name,'')
                FROM patients p
                LEFT JOIN doctors d
                ON p.doctor_id=d.id
                """
            )

        rows = cur.fetchall()
        conn.close()

        for row in rows:

            self.patient_tree.insert(
                "",
                "end",
                values=row
            )

    def search_patients(self):

        self.load_patients(
            self.patient_search.get()
        )

    def select_patient(self, event):

        selected = self.patient_tree.focus()

        if not selected:
            return

        values = self.patient_tree.item(
            selected,
            "values"
        )

        self.selected_patient_id = values[0]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM patients WHERE id=?",
            (values[0],)
        )

        row = cur.fetchone()

        conn.close()

        if row:

            keys = [
                "ID",
                "Name",
                "Age",
                "Gender",
                "Mobile",
                "Address",
                "Blood Group",
                "Disease",
                "Admission Date",
                "Doctor ID"
            ]

            self.clear_patient()

            self.selected_patient_id = row[0]

            for key, value in zip(
                keys[1:],
                row[1:]
            ):

                self.patient_entries[key].insert(
                    0,
                    "" if value is None
                    else str(value)
                )

    def update_patient(self):

        if not hasattr(
            self,
            "selected_patient_id"
        ):

            messagebox.showwarning(
                "Update",
                "Select a patient first."
            )

            return

        data = self.get_patient_data()

        try:

            age = (
                int(data["Age"])
                if data["Age"]
                else None
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Age must be a number."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE patients SET
            name=?,age=?,gender=?,mobile=?,
            address=?,blood_group=?,disease=?,
            admission_date=?,doctor_id=?
            WHERE id=?
            """,
            (
                data["Name"],
                age,
                data["Gender"],
                data["Mobile"],
                data["Address"],
                data["Blood Group"],
                data["Disease"],
                data["Admission Date"],
                data["Doctor ID"] or None,
                self.selected_patient_id
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Patient updated."
        )

        self.clear_patient()
        self.load_patients()

    def delete_patient(self):

        if not hasattr(
            self,
            "selected_patient_id"
        ):

            messagebox.showwarning(
                "Delete",
                "Select a patient first."
            )

            return

        if not messagebox.askyesno(
            "Confirm",
            "Delete selected patient?"
        ):
            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM patients WHERE id=?",
            (self.selected_patient_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Deleted",
            "Patient deleted."
        )

        self.clear_patient()
        self.load_patients()

    def clear_patient(self):

        if hasattr(
            self,
            "patient_entries"
        ):

            for entry in self.patient_entries.values():
                entry.delete(0, "end")

            self.patient_entries[
                "Admission Date"
            ].insert(
                0,
                str(date.today())
            )

        if hasattr(
            self,
            "selected_patient_id"
        ):

            del self.selected_patient_id

    # ========================================================
    # DOCTOR
    # ========================================================

    def doctor_module(self):

        self.clear_content()

        self.page_header(
            "Doctor Management",
            "Manage hospital doctors"
        )

        form = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=15
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        fields = [
            "Name",
            "Specialization",
            "Qualification",
            "Department",
            "Mobile",
            "Available Time"
        ]

        self.doctor_entries = {}

        for i, field in enumerate(fields):

            row = i // 3
            col = (i % 3) * 2

            ctk.CTkLabel(
                form,
                text=field,
                font=("Arial", 12, "bold"),
                text_color=TEXT
            ).grid(
                row=row,
                column=col,
                padx=10,
                pady=10
            )

            entry = ctk.CTkEntry(
                form,
                width=220,
                height=35
            )

            entry.grid(
                row=row,
                column=col + 1,
                padx=10,
                pady=10
            )

            self.doctor_entries[field] = entry

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack()

        self.colored_button(
            buttons,
            "➕ Add",
            GREEN,
            self.add_doctor
        )

        self.colored_button(
            buttons,
            "✏ Update",
            BLUE,
            self.update_doctor
        )

        self.colored_button(
            buttons,
            "🗑 Delete",
            RED,
            self.delete_doctor
        )

        self.colored_button(
            buttons,
            "🔄 Clear",
            ORANGE,
            self.clear_doctor
        )

        table = tk.Frame(
            self.content,
            bg=WHITE
        )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        columns = (
            "ID",
            "Name",
            "Specialization",
            "Qualification",
            "Department",
            "Mobile",
            "Available"
        )

        self.doctor_tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.doctor_tree.heading(
                col,
                text=col
            )

            self.doctor_tree.column(
                col,
                width=140
            )

        self.doctor_tree.pack(
            fill="both",
            expand=True
        )

        self.doctor_tree.bind(
            "<ButtonRelease-1>",
            self.select_doctor
        )

        self.load_doctors()

    def add_doctor(self):

        data = {
            key: value.get().strip()
            for key, value in
            self.doctor_entries.items()
        }

        if not data["Name"]:

            messagebox.showwarning(
                "Validation",
                "Doctor name required."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO doctors
            (
                name,specialization,qualification,
                department,mobile,available_time
            )
            VALUES(?,?,?,?,?,?)
            """,
            tuple(data.values())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Doctor added."
        )

        self.clear_doctor()
        self.load_doctors()

    def load_doctors(self):

        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id,name,specialization,
            qualification,department,mobile,
            available_time
            FROM doctors
            """
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.doctor_tree.insert(
                "",
                "end",
                values=row
            )

    def select_doctor(self, event):

        selected = self.doctor_tree.focus()

        if not selected:
            return

        values = self.doctor_tree.item(
            selected,
            "values"
        )

        self.clear_doctor()

        self.selected_doctor_id = values[0]

        for key, value in zip(
            self.doctor_entries.keys(),
            values[1:]
        ):

            self.doctor_entries[key].insert(
                0,
                value
            )

    def update_doctor(self):

        if not hasattr(
            self,
            "selected_doctor_id"
        ):

            messagebox.showwarning(
                "Update",
                "Select doctor first."
            )

            return

        data = {
            key: value.get().strip()
            for key, value in
            self.doctor_entries.items()
        }

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE doctors SET
            name=?,specialization=?,qualification=?,
            department=?,mobile=?,available_time=?
            WHERE id=?
            """,
            (
                *data.values(),
                self.selected_doctor_id
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Doctor updated."
        )

        self.clear_doctor()
        self.load_doctors()

    def delete_doctor(self):

        if not hasattr(
            self,
            "selected_doctor_id"
        ):

            messagebox.showwarning(
                "Delete",
                "Select doctor first."
            )

            return

        if not messagebox.askyesno(
            "Confirm",
            "Delete selected doctor?"
        ):
            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM doctors WHERE id=?",
            (self.selected_doctor_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Deleted",
            "Doctor deleted."
        )

        self.clear_doctor()
        self.load_doctors()

    def clear_doctor(self):

        if hasattr(
            self,
            "doctor_entries"
        ):

            for entry in self.doctor_entries.values():
                entry.delete(0, "end")

        if hasattr(
            self,
            "selected_doctor_id"
        ):

            del self.selected_doctor_id

    # ========================================================
    # APPOINTMENTS
    # ========================================================

    def appointment_module(self):

        self.clear_content()

        self.page_header(
            "Appointment Management",
            "Book and manage appointments"
        )

        form = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=15
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        fields = [
            "Patient ID",
            "Doctor ID",
            "Date",
            "Time",
            "Reason"
        ]

        self.appointment_entries = {}

        for i, field in enumerate(fields):

            ctk.CTkLabel(
                form,
                text=field,
                font=("Arial", 12, "bold"),
                text_color=TEXT
            ).grid(
                row=0,
                column=i,
                padx=10,
                pady=(12, 2)
            )

            entry = ctk.CTkEntry(
                form,
                width=180,
                height=35
            )

            entry.grid(
                row=1,
                column=i,
                padx=10,
                pady=(0, 12)
            )

            self.appointment_entries[field] = entry

        self.appointment_entries[
            "Date"
        ].insert(
            0,
            str(date.today())
        )

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack()

        self.colored_button(
            buttons,
            "📅 Book",
            GREEN,
            self.add_appointment
        )

        self.colored_button(
            buttons,
            "❌ Cancel",
            RED,
            self.cancel_appointment
        )

        self.colored_button(
            buttons,
            "🔄 Clear",
            ORANGE,
            self.clear_appointment
        )

        table = tk.Frame(
            self.content,
            bg=WHITE
        )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        columns = (
            "ID",
            "Patient",
            "Doctor",
            "Date",
            "Time",
            "Reason",
            "Status"
        )

        self.appointment_tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.appointment_tree.heading(
                col,
                text=col
            )

            self.appointment_tree.column(
                col,
                width=130
            )

        self.appointment_tree.pack(
            fill="both",
            expand=True
        )

        self.appointment_tree.bind(
            "<ButtonRelease-1>",
            self.select_appointment
        )

        self.load_appointments()

    def add_appointment(self):

        data = {
            key: value.get().strip()
            for key, value in
            self.appointment_entries.items()
        }

        if not data["Patient ID"] or not data["Doctor ID"]:

            messagebox.showwarning(
                "Validation",
                "Patient ID and Doctor ID required."
            )

            return

        try:

            patient_id = int(
                data["Patient ID"]
            )

            doctor_id = int(
                data["Doctor ID"]
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "IDs must be numbers."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM patients WHERE id=?",
            (patient_id,)
        )

        if not cur.fetchone():

            conn.close()

            messagebox.showerror(
                "Error",
                "Patient not found."
            )

            return

        cur.execute(
            "SELECT id FROM doctors WHERE id=?",
            (doctor_id,)
        )

        if not cur.fetchone():

            conn.close()

            messagebox.showerror(
                "Error",
                "Doctor not found."
            )

            return

        cur.execute(
            """
            INSERT INTO appointments
            (
                patient_id,doctor_id,
                appointment_date,
                appointment_time,
                reason,status
            )
            VALUES(?,?,?,?,?,'Booked')
            """,
            (
                patient_id,
                doctor_id,
                data["Date"],
                data["Time"],
                data["Reason"]
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment booked."
        )

        self.clear_appointment()
        self.load_appointments()

    def load_appointments(self):

        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
            a.id,
            COALESCE(p.name,''),
            COALESCE(d.name,''),
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status
            FROM appointments a
            LEFT JOIN patients p
            ON a.patient_id=p.id
            LEFT JOIN doctors d
            ON a.doctor_id=d.id
            ORDER BY a.id DESC
            """
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.appointment_tree.insert(
                "",
                "end",
                values=row
            )

    def select_appointment(self, event):

        selected = self.appointment_tree.focus()

        if selected:

            values = self.appointment_tree.item(
                selected,
                "values"
            )

            self.selected_appointment_id = values[0]

    def cancel_appointment(self):

        if not hasattr(
            self,
            "selected_appointment_id"
        ):

            messagebox.showwarning(
                "Cancel",
                "Select appointment first."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE appointments
            SET status='Cancelled'
            WHERE id=?
            """,
            (self.selected_appointment_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment cancelled."
        )

        self.load_appointments()

    def clear_appointment(self):

        for entry in self.appointment_entries.values():
            entry.delete(0, "end")

        self.appointment_entries[
            "Date"
        ].insert(
            0,
            str(date.today())
        )

    # ========================================================
    # MEDICINES
    # ========================================================

    def medicine_module(self):

        self.clear_content()

        self.page_header(
            "Medicine Management",
            "Manage pharmacy inventory"
        )

        form = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=15
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        fields = [
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Expiry Date"
        ]

        self.medicine_entries = {}

        for i, field in enumerate(fields):

            ctk.CTkLabel(
                form,
                text=field,
                font=("Arial", 12, "bold"),
                text_color=TEXT
            ).grid(
                row=0,
                column=i,
                padx=10,
                pady=10
            )

            entry = ctk.CTkEntry(
                form,
                width=190,
                height=35
            )

            entry.grid(
                row=1,
                column=i,
                padx=10,
                pady=10
            )

            self.medicine_entries[field] = entry

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack()

        self.colored_button(
            buttons,
            "➕ Add",
            GREEN,
            self.add_medicine
        )

        self.colored_button(
            buttons,
            "✏ Update",
            BLUE,
            self.update_medicine
        )

        self.colored_button(
            buttons,
            "🗑 Delete",
            RED,
            self.delete_medicine
        )

        self.colored_button(
            buttons,
            "⚠ Low Stock",
            ORANGE,
            self.low_stock
        )

        self.colored_button(
            buttons,
            "🔴 Expired",
            PURPLE,
            self.expired_medicines
        )

        self.colored_button(
            buttons,
            "🔄 All",
            BLUE,
            self.load_medicines
        )

        table = tk.Frame(
            self.content,
            bg=WHITE
        )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        columns = (
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Expiry"
        )

        self.medicine_tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.medicine_tree.heading(
                col,
                text=col
            )

            self.medicine_tree.column(
                col,
                width=140
            )

        self.medicine_tree.pack(
            fill="both",
            expand=True
        )

        self.medicine_tree.bind(
            "<ButtonRelease-1>",
            self.select_medicine
        )

        self.load_medicines()

    def add_medicine(self):

        data = {
            key: value.get().strip()
            for key, value in
            self.medicine_entries.items()
        }

        if not data["Name"]:

            messagebox.showwarning(
                "Validation",
                "Medicine name required."
            )

            return

        try:

            quantity = int(
                data["Quantity"] or 0
            )

            price = float(
                data["Price"] or 0
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid quantity or price."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO medicines
            (
                name,category,quantity,
                price,expiry_date
            )
            VALUES(?,?,?,?,?)
            """,
            (
                data["Name"],
                data["Category"],
                quantity,
                price,
                data["Expiry Date"]
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Medicine added."
        )

        self.clear_medicine()
        self.load_medicines()

    def load_medicines(self):

        if not hasattr(
            self,
            "medicine_tree"
        ):
            return

        for item in self.medicine_tree.get_children():
            self.medicine_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id,name,category,
            quantity,price,expiry_date
            FROM medicines
            """
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.medicine_tree.insert(
                "",
                "end",
                values=row
            )

    def select_medicine(self, event):

        selected = self.medicine_tree.focus()

        if not selected:
            return

        values = self.medicine_tree.item(
            selected,
            "values"
        )

        self.clear_medicine()

        self.selected_medicine_id = values[0]

        for key, value in zip(
            self.medicine_entries.keys(),
            values[1:]
        ):

            self.medicine_entries[key].insert(
                0,
                value
            )

    def update_medicine(self):

        if not hasattr(
            self,
            "selected_medicine_id"
        ):

            messagebox.showwarning(
                "Update",
                "Select medicine first."
            )

            return

        data = {
            key: value.get().strip()
            for key, value in
            self.medicine_entries.items()
        }

        try:

            quantity = int(
                data["Quantity"] or 0
            )

            price = float(
                data["Price"] or 0
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid quantity or price."
            )

            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE medicines SET
            name=?,category=?,quantity=?,
            price=?,expiry_date=?
            WHERE id=?
            """,
            (
                data["Name"],
                data["Category"],
                quantity,
                price,
                data["Expiry Date"],
                self.selected_medicine_id
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Medicine updated."
        )

        self.clear_medicine()
        self.load_medicines()

    def delete_medicine(self):

        if not hasattr(
            self,
            "selected_medicine_id"
        ):

            messagebox.showwarning(
                "Delete",
                "Select medicine first."
            )

            return

        if not messagebox.askyesno(
            "Confirm",
            "Delete medicine?"
        ):
            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM medicines WHERE id=?",
            (self.selected_medicine_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Deleted",
            "Medicine deleted."
        )

        self.clear_medicine()
        self.load_medicines()

    def low_stock(self):

        for item in self.medicine_tree.get_children():
            self.medicine_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id,name,category,
            quantity,price,expiry_date
            FROM medicines
            WHERE quantity <= 10
            """
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.medicine_tree.insert(
                "",
                "end",
                values=row
            )

    def expired_medicines(self):

        for item in self.medicine_tree.get_children():
            self.medicine_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id,name,category,
            quantity,price,expiry_date
            FROM medicines
            WHERE expiry_date != ''
            AND expiry_date < ?
            """,
            (str(date.today()),)
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.medicine_tree.insert(
                "",
                "end",
                values=row
            )

    def clear_medicine(self):

        if hasattr(
            self,
            "medicine_entries"
        ):

            for entry in self.medicine_entries.values():
                entry.delete(0, "end")

        if hasattr(
            self,
            "selected_medicine_id"
        ):

            del self.selected_medicine_id

    # ========================================================
    # BILLING
    # ========================================================

    def billing_module(self):

        self.clear_content()

        self.page_header(
            "Billing Management",
            "Generate hospital bills"
        )

        form = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=15
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        fields = [
            "Patient ID",
            "Doctor Fee",
            "Medicine Charges",
            "Room Charges",
            "Other Charges"
        ]

        self.bill_entries = {}

        for i, field in enumerate(fields):

            ctk.CTkLabel(
                form,
                text=field,
                font=("Arial", 12, "bold"),
                text_color=TEXT
            ).grid(
                row=0,
                column=i,
                padx=10,
                pady=10
            )

            entry = ctk.CTkEntry(
                form,
                width=190,
                height=35
            )

            entry.grid(
                row=1,
                column=i,
                padx=10,
                pady=10
            )

            self.bill_entries[field] = entry

        self.total_label = ctk.CTkLabel(
            form,
            text="TOTAL: ₹0.00",
            font=("Arial", 20, "bold"),
            text_color=GREEN
        )

        self.total_label.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        self.colored_button(
            form,
            "🧮 Calculate",
            BLUE,
            self.calculate_bill
        )

        self.colored_button(
            form,
            "🧾 Generate",
            GREEN,
            self.generate_bill
        )

        table = tk.Frame(
            self.content,
            bg=WHITE
        )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        columns = (
            "ID",
            "Patient",
            "Doctor Fee",
            "Medicine",
            "Room",
            "Other",
            "Total",
            "Status",
            "Date"
        )

        self.bill_tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.bill_tree.heading(
                col,
                text=col
            )

            self.bill_tree.column(
                col,
                width=115
            )

        self.bill_tree.pack(
            fill="both",
            expand=True
        )

        self.load_bills()

    def calculate_bill(self):

        try:

            doctor = float(
                self.bill_entries[
                    "Doctor Fee"
                ].get() or 0
            )

            medicine = float(
                self.bill_entries[
                    "Medicine Charges"
                ].get() or 0
            )

            room = float(
                self.bill_entries[
                    "Room Charges"
                ].get() or 0
            )

            other = float(
                self.bill_entries[
                    "Other Charges"
                ].get() or 0
            )

            total = (
                doctor +
                medicine +
                room +
                other
            )

            self.current_total = total

            self.total_label.configure(
                text=f"TOTAL: ₹{total:.2f}"
            )

            return total

        except ValueError:

            messagebox.showerror(
                "Error",
                "Charges must be numbers."
            )

            return None

    def generate_bill(self):

        patient = self.bill_entries[
            "Patient ID"
        ].get().strip()

        if not patient:

            messagebox.showwarning(
                "Validation",
                "Patient ID required."
            )

            return

        try:

            patient_id = int(patient)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Patient ID must be number."
            )

            return

        total = self.calculate_bill()

        if total is None:
            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM patients WHERE id=?",
            (patient_id,)
        )

        if not cur.fetchone():

            conn.close()

            messagebox.showerror(
                "Error",
                "Patient not found."
            )

            return

        doctor = float(
            self.bill_entries[
                "Doctor Fee"
            ].get() or 0
        )

        medicine = float(
            self.bill_entries[
                "Medicine Charges"
            ].get() or 0
        )

        room = float(
            self.bill_entries[
                "Room Charges"
            ].get() or 0
        )

        other = float(
            self.bill_entries[
                "Other Charges"
            ].get() or 0
        )

        cur.execute(
            """
            INSERT INTO bills
            (
                patient_id,
                doctor_fee,
                medicine_charges,
                room_charges,
                other_charges,
                total_amount,
                payment_status,
                bill_date
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                patient_id,
                doctor,
                medicine,
                room,
                other,
                total,
                "Pending",
                str(date.today())
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            f"Bill generated successfully.\n\n"
            f"Total Amount: ₹{total:.2f}"
        )

        self.clear_bill()
        self.load_bills()

    def load_bills(self):

        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
            b.id,
            COALESCE(p.name,''),
            b.doctor_fee,
            b.medicine_charges,
            b.room_charges,
            b.other_charges,
            b.total_amount,
            b.payment_status,
            b.bill_date
            FROM bills b
            LEFT JOIN patients p
            ON b.patient_id=p.id
            ORDER BY b.id DESC
            """
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.bill_tree.insert(
                "",
                "end",
                values=row
            )

    def clear_bill(self):

        for entry in self.bill_entries.values():
            entry.delete(0, "end")

        self.total_label.configure(
            text="TOTAL: ₹0.00"
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    create_database()

    root = ctk.CTk()

    app = HospitalApp(root)

    root.mainloop()