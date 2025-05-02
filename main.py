import tkinter as tk
import home
from database import FlightDatabase

def main():
    # Create main window
    root = tk.Tk()
    
    # Set up home page
    home.HomePage(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
