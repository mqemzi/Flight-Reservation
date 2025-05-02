import tkinter as tk
import home
from database import FlightDatabase

def initialize_database():
    """Initialize the database with some sample flights."""
    db = FlightDatabase()
    
    # Add some sample flights if none exist
    db.cursor.execute('SELECT COUNT(*) FROM flights')
    if db.cursor.fetchone()[0] == 0:
        sample_flights = [
            ('FL001', 'New York', 'Los Angeles', '2025-06-15 10:00', 50),
            ('FL002', 'Chicago', 'Miami', '2025-06-16 14:30', 40),
            ('FL003', 'San Francisco', 'Seattle', '2025-06-17 09:45', 30),
            ('FL004', 'Boston', 'Houston', '2025-06-18 11:15', 45)
        ]
        
        for flight in sample_flights:
            db.add_flight(flight[0], flight[1], flight[2], flight[3], flight[4])
    
    db.conn.commit()
    db.close()

def main():
    # Initialize database with sample data
    initialize_database()
    
    # Create main window
    root = tk.Tk()
    
    # Set up home page
    home.HomePage(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
