import tkinter as tk
from tkinter import ttk
import booking
import reservations

class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("Flight Reservation System")
        master.geometry("500x400")
        master.configure(bg='#f0f0f0')

        # Title
        title_label = tk.Label(master, text="Flight Reservation System", 
                               font=("Arial", 20, "bold"), 
                               bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)

        # Frame for buttons
        button_frame = tk.Frame(master, bg='#f0f0f0')
        button_frame.pack(expand=True)

        # Book Flight Button
        book_button = tk.Button(button_frame, text="Book Flight", 
                                command=self.open_booking_page,
                                width=20, height=2, 
                                bg='#4CAF50', fg='white', 
                                font=("Arial", 12, "bold"))
        book_button.pack(pady=10)

        # View Reservations Button
        view_button = tk.Button(button_frame, text="View Reservations", 
                                command=self.open_reservations_page,
                                width=20, height=2, 
                                bg='#2196F3', fg='white', 
                                font=("Arial", 12, "bold"))
        view_button.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(button_frame, text="Exit", 
                                command=master.quit,
                                width=20, height=2, 
                                bg='#F44336', fg='white', 
                                font=("Arial", 12, "bold"))
        exit_button.pack(pady=10)

    def open_booking_page(self):
        booking_window = tk.Toplevel(self.master)
        booking.BookingPage(booking_window)

    def open_reservations_page(self):
        reservations_window = tk.Toplevel(self.master)
        reservations.ReservationsPage(reservations_window)

def run():
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
