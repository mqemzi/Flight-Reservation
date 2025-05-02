import tkinter as tk
from tkinter import ttk, messagebox
import booking
import reservations

class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("Flight Reservation System")
        master.geometry("600x500")
        master.configure(bg='#f0f0f0')

        # Configure grid layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)

        # Header
        header_frame = tk.Frame(master, bg='#4CAF50', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="Flight Reservation System", 
                               font=("Arial", 24, "bold"), 
                               bg='#4CAF50', fg='white')
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Main Content Frame
        content_frame = tk.Frame(master, bg='#f0f0f0')
        content_frame.grid(row=1, column=0, padx=50, pady=30, sticky='nsew')
        content_frame.grid_columnconfigure(0, weight=1)

        # Button Styles
        button_style = {
            'width': 30,
            'height': 3,
            'font': ("Arial", 12, "bold"),
            'relief': tk.FLAT,
            'cursor': 'hand2'
        }

        # Book Flight Button
        book_button = tk.Button(content_frame, text="Book Flight", 
                                command=self.open_booking_page,
                                bg='#2196F3', fg='white', **button_style)
        book_button.grid(row=0, column=0, pady=10)

        # View Reservations Button
        view_button = tk.Button(content_frame, text="View Reservations", 
                                command=self.open_reservations_page,
                                bg='#FF9800', fg='white', **button_style)
        view_button.grid(row=1, column=0, pady=10)

        # Exit Button
        exit_button = tk.Button(content_frame, text="Exit Application", 
                                command=self.confirm_exit,
                                bg='#F44336', fg='white', **button_style)
        exit_button.grid(row=2, column=0, pady=10)

        # Footer
        footer_frame = tk.Frame(master, bg='#333333', height=50)
        footer_frame.grid(row=2, column=0, sticky='ew')
        footer_frame.grid_propagate(False)

        footer_label = tk.Label(footer_frame, 
                                text="© 2025 Flight Reservation System", 
                                bg='#333333', fg='white', 
                                font=("Arial", 10))
        footer_label.place(relx=0.5, rely=0.5, anchor='center')

    def open_booking_page(self):
        booking_window = tk.Toplevel(self.master)
        booking_window.title("Book a Flight")
        booking.BookingPage(booking_window)

    def open_reservations_page(self):
        reservations_window = tk.Toplevel(self.master)
        reservations_window.title("My Reservations")
        reservations.ReservationsPage(reservations_window)

    def confirm_exit(self):
        """Confirm before exiting the application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
            self.master.quit()

def run():
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
