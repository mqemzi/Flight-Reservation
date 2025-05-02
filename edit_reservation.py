import tkinter as tk
from tkinter import messagebox, ttk
from database import FlightDatabase
from datetime import datetime
import re

class EditReservationPage:
    def __init__(self, master, reservation_details, refresh_callback):
        self.master = master
        self.master.title("Edit Reservation")
        self.master.geometry("600x700")
        self.master.configure(bg='#f0f0f0')

        # Configure grid layout
        master.grid_columnconfigure(0, weight=1)

        # Database connection
        self.db = FlightDatabase()

        # Reservation details
        self.reservation_id = reservation_details[0]

        # Refresh callback
        self.refresh_callback = refresh_callback

        # Header
        header_frame = tk.Frame(master, bg='#2196F3', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="Edit Reservation", 
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
            entry.bind('<KeyRelease>', lambda e, label=label_text: self.validate_input(e, label))

            self.entries[label_text] = entry

        # Populate initial values
        self.entries["Name"].insert(0, reservation_details[1])
        self.entries["Flight Number"].insert(0, reservation_details[2])
        self.entries["Departure"].insert(0, reservation_details[3])
        self.entries["Destination"].insert(0, reservation_details[4])
        self.entries["Date"].insert(0, reservation_details[5])
        self.entries["Seat Number"].insert(0, reservation_details[6])

        # Update Button
        update_button = tk.Button(form_frame, text="Update Reservation", 
                                  command=self.update_reservation,
                                  width=30, height=2, 
                                  bg='#4CAF50', fg='white', 
                                  font=("Arial", 14, "bold"), 
                                  relief=tk.FLAT)
        update_button.grid(row=len(input_fields), column=0, columnspan=2, pady=20)

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

    def update_reservation(self):
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

        # Update reservation
        result = self.db.update_reservation(
            reservation_id=self.reservation_id,
            name=name,
            flight_number=flight_number,
            departure=departure,
            destination=destination,
            date=date,
            seat_number=seat_number
        )

        if result:
            # Refresh reservations list
            self.refresh_callback()

            # Close edit window
            messagebox.showinfo("Success", "Reservation updated successfully")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Unable to update reservation. Please check your details.")


