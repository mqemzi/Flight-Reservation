import tkinter as tk
from tkinter import messagebox, ttk
from database import FlightDatabase
import sqlite3
from datetime import datetime

class BookingPage:
    def __init__(self, master):
        self.master = master
        master.title("Book a Flight")
        master.geometry("500x600")
        master.configure(bg='#f0f0f0')

        # Database connection
        self.db = FlightDatabase()

        # Title
        title_label = tk.Label(master, text="Flight Booking", 
                               font=("Arial", 18, "bold"), 
                               bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)

        # Booking Form Frame
        form_frame = tk.Frame(master, bg='#f0f0f0')
        form_frame.pack(padx=30, fill='x')

        # Input Fields
        labels = ["Name", "Email", "Flight Number", "Origin", "Destination", "Departure Date"]
        self.entries = {}

        for label_text in labels:
            row_frame = tk.Frame(form_frame, bg='#f0f0f0')
            row_frame.pack(fill='x', pady=5)

            label = tk.Label(row_frame, text=label_text, width=15, anchor='w', 
                             bg='#f0f0f0', font=("Arial", 10))
            label.pack(side='left')

            entry = tk.Entry(row_frame, width=30, font=("Arial", 10))
            entry.pack(side='right')
            self.entries[label_text] = entry

        # Available Flights Section
        available_flights_label = tk.Label(master, text="Available Flights", 
                                           font=("Arial", 12, "bold"), 
                                           bg='#f0f0f0', fg='#333333')
        available_flights_label.pack(pady=10)

        # Treeview for Available Flights
        self.flights_tree = ttk.Treeview(master, columns=('Flight', 'Origin', 'Destination', 'Departure'), show='headings')
        self.flights_tree.heading('Flight', text='Flight Number')
        self.flights_tree.heading('Origin', text='Origin')
        self.flights_tree.heading('Destination', text='Destination')
        self.flights_tree.heading('Departure', text='Departure Date')
        self.flights_tree.pack(padx=20, fill='x')

        # Populate Available Flights
        self.populate_available_flights()

        # Book Button
        book_button = tk.Button(master, text="Book Flight", 
                                command=self.book_flight,
                                width=20, height=2, 
                                bg='#4CAF50', fg='white', 
                                font=("Arial", 12, "bold"))
        book_button.pack(pady=20)

    def populate_available_flights(self):
        # Clear existing items
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)

        # Get available flights from database
        flights = self.db.get_available_flights()
        for flight in flights:
            self.flights_tree.insert('', 'end', values=(
                flight[1],  # flight_number
                flight[2],  # origin
                flight[3],  # destination
                flight[4]   # departure_time
            ))

    def book_flight(self):
        # Validate input
        required_fields = ["Name", "Email", "Flight Number"]
        for field in required_fields:
            if not self.entries[field].get().strip():
                messagebox.showerror("Error", f"{field} is required")
                return

        # Find flight ID based on flight number
        flight_number = self.entries["Flight Number"].get()
        
        try:
            # Make reservation
            result = self.db.make_reservation(
                flight_id=self.get_flight_id(flight_number),
                passenger_name=self.entries["Name"].get(),
                passenger_email=self.entries["Email"].get()
            )

            if result:
                messagebox.showinfo("Success", "Flight booked successfully!")
                # Refresh available flights
                self.populate_available_flights()
                # Clear entries
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Unable to book flight. Flight might be full.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_flight_id(self, flight_number):
        # Fetch flight ID from database
        self.db.cursor.execute('SELECT flight_id FROM flights WHERE flight_number = ?', (flight_number,))
        result = self.db.cursor.fetchone()
        if result:
            return result[0]
        raise ValueError(f"Flight {flight_number} not found")
