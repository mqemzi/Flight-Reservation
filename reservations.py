import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import FlightDatabase
import edit_reservation

class ReservationsPage:
    def __init__(self, master):
        self.master = master
        master.title("My Reservations")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        # Database connection
        self.db = FlightDatabase()

        # Title
        title_label = tk.Label(master, text="My Reservations", 
                               font=("Arial", 18, "bold"), 
                               bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)

        # Treeview for Reservations
        self.reservations_tree = ttk.Treeview(master, 
            columns=('ID', 'Name', 'Email', 'Flight', 'Seat'), 
            show='headings'
        )
        self.reservations_tree.heading('ID', text='Reservation ID')
        self.reservations_tree.heading('Name', text='Passenger Name')
        self.reservations_tree.heading('Email', text='Email')
        self.reservations_tree.heading('Flight', text='Flight Number')
        self.reservations_tree.heading('Seat', text='Seat Number')
        
        # Set column widths
        self.reservations_tree.column('ID', width=100, anchor='center')
        self.reservations_tree.column('Name', width=150)
        self.reservations_tree.column('Email', width=200)
        self.reservations_tree.column('Flight', width=100, anchor='center')
        self.reservations_tree.column('Seat', width=100, anchor='center')
        
        self.reservations_tree.pack(padx=20, pady=10, fill='both', expand=True)

        # Buttons Frame
        button_frame = tk.Frame(master, bg='#f0f0f0')
        button_frame.pack(pady=10)

        # Edit Button
        edit_button = tk.Button(button_frame, text="Edit Reservation", 
                                command=self.edit_reservation,
                                width=15, height=2, 
                                bg='#2196F3', fg='white', 
                                font=("Arial", 10, "bold"))
        edit_button.pack(side='left', padx=5)

        # Delete Button
        delete_button = tk.Button(button_frame, text="Delete Reservation", 
                                  command=self.delete_reservation,
                                  width=15, height=2, 
                                  bg='#F44336', fg='white', 
                                  font=("Arial", 10, "bold"))
        delete_button.pack(side='left', padx=5)

        # Populate Reservations
        self.populate_reservations()

    def populate_reservations(self):
        # Clear existing items
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)

        # Fetch reservations
        try:
            self.db.cursor.execute('''
                SELECT 
                    r.reservation_id, 
                    r.passenger_name, 
                    r.passenger_email, 
                    f.flight_number, 
                    r.seat_number 
                FROM 
                    reservations r
                JOIN 
                    flights f ON r.flight_id = f.flight_id
            ''')
            reservations = self.db.cursor.fetchall()

            for reservation in reservations:
                self.reservations_tree.insert('', 'end', values=reservation)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def edit_reservation(self):
        # Get selected reservation
        selected_item = self.reservations_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a reservation to edit")
            return

        # Get reservation details
        reservation_details = self.reservations_tree.item(selected_item)['values']
        
        # Open edit window
        edit_window = tk.Toplevel(self.master)
        edit_reservation.EditReservationPage(edit_window, reservation_details, self.populate_reservations)

    def delete_reservation(self):
        # Get selected reservation
        selected_item = self.reservations_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a reservation to delete")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?")
        if not confirm:
            return

        # Get reservation ID
        reservation_id = self.reservations_tree.item(selected_item)['values'][0]

        try:
            # Delete reservation and update available seats
            self.db.cursor.execute('''
                DELETE FROM reservations WHERE reservation_id = ?
            ''', (reservation_id,))
            self.db.conn.commit()

            # Refresh reservations list
            self.populate_reservations()
            messagebox.showinfo("Success", "Reservation deleted successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
