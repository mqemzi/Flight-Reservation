import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from database import FlightDatabase
from datetime import datetime
import re

class BookingPage:
    def __init__(self, master):
        self.master = master
        master.title("Book a Flight")
        master.geometry("600x700")
        master.configure(bg='#f0f0f0')

        # Database connection
        self.db = FlightDatabase()

        # Configure grid layout
        master.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = tk.Frame(master, bg='#2196F3', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="Book a Flight", 
                               font=("Arial", 24, "bold"), 
                               bg='#2196F3', fg='white')
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Form Frame
        form_frame = tk.Frame(master, bg='#f0f0f0')
        form_frame.grid(row=1, column=0, padx=50, pady=30, sticky='nsew')
        form_frame.grid_columnconfigure(1, weight=1)

        # Input Fields
        input_fields = [
            ("Name", "Enter full name"),
            ("Flight Number", "e.g. FL001"),
            ("Departure", "City of departure"),
            ("Destination", "City of arrival"),
            ("Date", "YYYY-MM-DD"),
            ("Seat Number", "e.g. 12A, 15B")
        ]

        self.entries = {}
        validation_funcs = {
            "Name": self.validate_name,
            "Flight Number": self.validate_flight_number,
            "Departure": self.validate_location,
            "Destination": self.validate_location,
            "Date": self.validate_date,
            "Seat Number": self.validate_seat_number
        }

        for row, (label_text, placeholder) in enumerate(input_fields):
            label = tk.Label(form_frame, text=label_text, 
                             font=("Arial", 12), 
                             bg='#f0f0f0', fg='#333333', anchor='w')
            label.grid(row=row, column=0, sticky='w', padx=(0,10), pady=10)

            entry = tk.Entry(form_frame, width=40, 
                             font=("Arial", 12), 
                             relief=tk.FLAT, 
                             highlightthickness=1, 
                             highlightcolor='#2196F3')
            entry.grid(row=row, column=1, sticky='ew', pady=10)
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e, entry=entry: self.on_entry_click(e, entry))
            entry.bind('<FocusOut>', lambda e, entry=entry, label=label_text: self.on_entry_leave(e, entry, label))
            entry.bind('<KeyRelease>', lambda e, label=label_text: self.validate_input(e, label))

            self.entries[label_text] = entry

        # Submit Button
        submit_button = tk.Button(form_frame, text="Book Reservation", 
                                  command=self.submit_reservation,
                                  width=30, height=2, 
                                  bg='#4CAF50', fg='white', 
                                  font=("Arial", 14, "bold"), 
                                  relief=tk.FLAT)
        submit_button.grid(row=len(input_fields), column=0, columnspan=2, pady=20)

    def on_entry_click(self, event, entry):
        """Remove placeholder text when entry is clicked"""
        if entry.get() in ["Enter full name", "e.g. FL001", "City of departure", 
                           "City of arrival", "YYYY-MM-DD", "e.g. 12A, 15B"]:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_entry_leave(self, event, entry, label):
        """Restore placeholder if no text is entered"""
        if entry.get().strip() == "":
            placeholders = {
                "Name": "Enter full name",
                "Flight Number": "e.g. FL001",
                "Departure": "City of departure",
                "Destination": "City of arrival",
                "Date": "YYYY-MM-DD",
                "Seat Number": "e.g. 12A, 15B"
            }
            entry.insert(0, placeholders[label])
            entry.config(fg='gray')

    def validate_input(self, event, label):
        """Validate input in real-time"""
        validation_funcs = {
            "Name": self.validate_name,
            "Flight Number": self.validate_flight_number,
            "Departure": self.validate_location,
            "Destination": self.validate_location,
            "Date": self.validate_date,
            "Seat Number": self.validate_seat_number
        }
        validation_funcs[label]()

    def validate_name(self):
        name = self.entries["Name"].get().strip()
        if not name or len(name.split()) < 2:
            self.entries["Name"].config(fg='red')
            return False
        self.entries["Name"].config(fg='green')
        return True

    def validate_flight_number(self):
        flight_number = self.entries["Flight Number"].get().strip()
        pattern = r'^FL\d{3}$'
        if not re.match(pattern, flight_number):
            self.entries["Flight Number"].config(fg='red')
            return False
        self.entries["Flight Number"].config(fg='green')
        return True

    def validate_location(self, field="Departure"):
        location = self.entries[field].get().strip()
        if not location or len(location) < 2:
            self.entries[field].config(fg='red')
            return False
        self.entries[field].config(fg='green')
        return True

    def validate_date(self):
        date_str = self.entries["Date"].get().strip()
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date < datetime.now():
                self.entries["Date"].config(fg='red')
                return False
            self.entries["Date"].config(fg='green')
            return True
        except ValueError:
            self.entries["Date"].config(fg='red')
            return False

    def validate_seat_number(self):
        seat_number = self.entries["Seat Number"].get().strip()
        pattern = r'^\d{1,2}[A-F]$'
        if not re.match(pattern, seat_number):
            self.entries["Seat Number"].config(fg='red')
            return False
        self.entries["Seat Number"].config(fg='green')
        return True

    def submit_reservation(self):
        # Validate all inputs
        validation_results = [
            self.validate_name(),
            self.validate_flight_number(),
            self.validate_location("Departure"),
            self.validate_location("Destination"),
            self.validate_date(),
            self.validate_seat_number()
        ]

        if not all(validation_results):
            messagebox.showerror("Validation Error", "Please correct the highlighted fields")
            return

        # Get validated inputs
        name = self.entries["Name"].get().strip()
        flight_number = self.entries["Flight Number"].get().strip()
        departure = self.entries["Departure"].get().strip()
        destination = self.entries["Destination"].get().strip()
        date = self.entries["Date"].get().strip()
        seat_number = self.entries["Seat Number"].get().strip()

        # Add reservation to database
        result = self.db.add_reservation(name, flight_number, departure, destination, date, seat_number)

        if result:
            messagebox.showinfo("Success", "Reservation added successfully")
            # Clear entries after successful booking
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                placeholders = {
                    "Name": "Enter full name",
                    "Flight Number": "e.g. FL001",
                    "Departure": "City of departure",
                    "Destination": "City of arrival",
                    "Date": "YYYY-MM-DD",
                    "Seat Number": "e.g. 12A, 15B"
                }
                entry.insert(0, placeholders[entry.cget('text')])
                entry.config(fg='gray')
        else:
            messagebox.showerror("Error", "Failed to add reservation. Seat might be already taken.")


