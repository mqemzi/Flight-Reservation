import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from database import FlightDatabase
import edit_reservation

class ReservationsPage:
    def __init__(self, master):
        self.master = master
        master.title("My Reservations")
        master.geometry("1000x600")
        master.configure(bg='#f0f0f0')

        # Configure grid layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)

        # Header
        header_frame = tk.Frame(master, bg='#2196F3', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="My Reservations", 
                               font=("Arial", 24, "bold"), 
                               bg='#2196F3', fg='white')
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Reservations Frame
        reservations_frame = tk.Frame(master, bg='#f0f0f0')
        reservations_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
        reservations_frame.grid_columnconfigure(0, weight=1)
        reservations_frame.grid_rowconfigure(0, weight=1)

        # Reservations Tree View
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme
        style.configure('Treeview', 
                        background='#f0f0f0', 
                        foreground='black', 
                        rowheight=35,
                        fieldbackground='#f0f0f0')
        style.map('Treeview', 
                  background=[('selected', '#2196F3')], 
                  foreground=[('selected', 'white')])

        self.reservations_tree = ttk.Treeview(reservations_frame, 
                                              columns=(
                                                  "ID", "Name", "Flight Number", 
                                                  "Departure", "Destination", "Date", "Seat Number"
                                              ), 
                                              show='headings')

        # Scrollbar
        scrollbar = ttk.Scrollbar(reservations_frame, orient='vertical', command=self.reservations_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.reservations_tree.configure(yscroll=scrollbar.set)

        # Define headings
        headings = [
            ("ID", 50), 
            ("Name", 150), 
            ("Flight Number", 100), 
            ("Departure", 100), 
            ("Destination", 100), 
            ("Date", 100), 
            ("Seat Number", 100)
        ]
        for heading, width in headings:
            self.reservations_tree.heading(heading, text=heading, command=lambda col=heading: self.sort_column(col, False))
            self.reservations_tree.column(heading, width=width, anchor='center')

        self.reservations_tree.grid(row=0, column=0, sticky='nsew')

        # Bind double-click to edit
        self.reservations_tree.bind('<Double-1>', self.edit_reservation)

        # Buttons Frame
        button_frame = tk.Frame(master, bg='#f0f0f0')
        button_frame.grid(row=2, column=0, pady=10)

        # Button Style
        button_style = {
            'width': 20, 
            'height': 2, 
            'font': ("Arial", 12, "bold"), 
            'relief': tk.FLAT
        }

        # Edit Button
        edit_button = tk.Button(button_frame, text="Edit Reservation", 
                                command=self.edit_reservation_click,
                                bg='#4CAF50', fg='white', **button_style)
        edit_button.pack(side='left', padx=10)

        # Delete Button
        delete_button = tk.Button(button_frame, text="Delete Reservation", 
                                  command=self.delete_reservation,
                                  bg='#F44336', fg='white', **button_style)
        delete_button.pack(side='left', padx=10)

        # Database connection
        self.db = FlightDatabase()

        # Populate Reservations
        self.populate_reservations()

    def sort_column(self, col, reverse):
        """Sort treeview columns when header is clicked"""
        l = [(self.reservations_tree.set(k, col), k) for k in self.reservations_tree.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.reservations_tree.move(k, '', index)

        # Toggle sort direction
        self.reservations_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def populate_reservations(self):
        # Clear existing items
        for i in self.reservations_tree.get_children():
            self.reservations_tree.delete(i)

        # Fetch and display reservations
        reservations = self.db.get_all_reservations()
        for reservation in reservations:
            self.reservations_tree.insert('', 'end', values=reservation)

    def edit_reservation_click(self):
        """Handles edit button click"""
        selected_item = self.reservations_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a reservation to edit")
            return

        # Get reservation details
        reservation_details = self.reservations_tree.item(selected_item)['values']

        # Open edit window
        edit_window = tk.Toplevel(self.master)
        edit_page = edit_reservation.EditReservationPage(edit_window, reservation_details, self.populate_reservations)

    def edit_reservation(self, event):
        """Handles double-click edit"""
        # Get selected item
        selected_item = self.reservations_tree.selection()
        if not selected_item:
            return

        # Get reservation details
        reservation_details = self.reservations_tree.item(selected_item)['values']

        # Open edit window
        edit_window = tk.Toplevel(self.master)
        edit_page = edit_reservation.EditReservationPage(edit_window, reservation_details, self.populate_reservations)

    def delete_reservation(self):
        # Get selected reservation
        selected_item = self.reservations_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a reservation to delete")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?")
        if confirm:
            # Get reservation ID
            reservation_id = self.reservations_tree.item(selected_item)['values'][0]

            # Delete from database
            result = self.db.delete_reservation(reservation_id)

            if result:
                messagebox.showinfo("Success", "Reservation deleted successfully")
                self.populate_reservations()
            else:
                messagebox.showerror("Error", "Failed to delete reservation")
