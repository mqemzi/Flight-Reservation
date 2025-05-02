# Flight Reservation Desktop App

## Overview
A comprehensive desktop application for managing flight reservations, built with Python, Tkinter, and SQLite.

## Features
- Book new flight reservations
- View all current reservations
- Edit existing reservations
- Delete reservations
- User-friendly graphical interface

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/flight-reservation-app.git
cd flight-reservation-app
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python main.py
```

## Building Executable
To create a standalone executable:
```bash
pyinstaller --onefile main.py
```
The executable will be located in the `dist/` directory.

## Application Pages
1. **Home Page**: 
   - Book Flight
   - View Reservations
   - Exit Application

2. **Booking Page**:
   - Enter passenger details
   - Select available flights
   - Book a flight

3. **Reservations Page**:
   - View all reservations
   - Edit existing reservations
   - Delete reservations

## Technologies Used
- Python 3.x
- Tkinter (GUI)
- SQLite (Database)
- PyInstaller (Packaging)

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
