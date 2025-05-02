import tkinter as tk
from tkinter import messagebox
from database import FlightDatabase
import sqlite3

class EditReservationPage:
    def __init__(self, master, reservation_details, refresh_callback):
        self.master = master
        self.master.title("Edit Reservation")
        self.master.geometry("500x400")
        self.master.configure(bg='#f0f0f0')

        # Database connection
        self.db = FlightDatabase()

        # Reservation details
        self.reservation_id = reservation_details[0]
        self.original_flight_number = reservation_details[3]

        # Refresh callback
        self.refresh_callback = refresh_callback

        # Title
        title_label = tk.Label(master, text="Edit Reservation", 
                               font=("Arial", 18, "bold"), 
                               bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)

        # Input Fields
        labels = ["Passenger Name", "Passenger Email", "Flight Number"]
        self.entries = {}

        for label_text in labels:
            row_frame = tk.Frame(master, bg='#f0f0f0')
            row_frame.pack(fill='x', padx=30, pady=5)

            label = tk.Label(row_frame, text=label_text, width=15, anchor='w', 
                             bg='#f0f0f0', font=("Arial", 10))
            label.pack(side='left')

            entry = tk.Entry(row_frame, width=30, font=("Arial", 10))
            entry.pack(side='right')
            self.entries[label_text] = entry

        # Populate initial values
        self.entries["Passenger Name"].insert(0, reservation_details[1])
        self.entries["Passenger Email"].insert(0, reservation_details[2])
        self.entries["Flight Number"].insert(0, reservation_details[3])

        # Update Button
        update_button = tk.Button(master, text="Update Reservation", 
                                  command=self.update_reservation,
                                  width=20, height=2, 
                                  bg='#4CAF50', fg='white', 
                                  font=("Arial", 12, "bold"))
        update_button.pack(pady=20)

    def update_reservation(self):
        # Validate input
        name = self.entries["Passenger Name"].get().strip()
        email = self.entries["Passenger Email"].get().strip()
        flight_number = self.entries["Flight Number"].get().strip()

        if not name or not email or not flight_number:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Find new flight ID
            self.db.cursor.execute('SELECT flight_id FROM flights WHERE flight_number = ?', (flight_number,))
            new_flight_result = self.db.cursor.fetchone()

            if not new_flight_result:
                messagebox.showerror("Error", f"Flight {flight_number} not found")
                return

            new_flight_id = new_flight_result[0]

            # Update reservation
            self.db.cursor.execute('''
                UPDATE reservations 
                SET passenger_name = ?, 
                    passenger_email = ?, 
                    flight_id = ? 
                WHERE reservation_id = ?
            ''', (name, email, new_flight_id, self.reservation_id))

            # Commit changes
            self.db.conn.commit()

            # Refresh reservations list
            self.refresh_callback()

            # Close edit window
            messagebox.showinfo("Success", "Reservation updated successfully")
            self.master.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
