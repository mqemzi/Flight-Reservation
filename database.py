import sqlite3
import os
from datetime import datetime

class FlightDatabase:
    def __init__(self, db_path=None):
        # Use the absolute path to ensure consistency
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'flights.db')
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables for flight reservations."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL,
                UNIQUE(flight_number, seat_number)
            )
        ''')
        self.conn.commit()

    def add_reservation(self, name, flight_number, departure, destination, date, seat_number):
        """Add a new reservation to the database."""
        try:
            # Check if seat is already taken
            self.cursor.execute('''
                SELECT COUNT(*) FROM reservations 
                WHERE flight_number = ? AND seat_number = ?
            ''', (flight_number, seat_number))
            
            if self.cursor.fetchone()[0] > 0:
                return False  # Seat is already taken
            
            # Insert new reservation
            self.cursor.execute('''
                INSERT INTO reservations 
                (name, flight_number, departure, destination, date, seat_number) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, flight_number, departure, destination, date, seat_number))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_reservations(self):
        """Retrieve all reservations."""
        self.cursor.execute('SELECT * FROM reservations')
        return self.cursor.fetchall()

    def update_reservation(self, reservation_id, name=None, flight_number=None, 
                           departure=None, destination=None, date=None, seat_number=None):
        """Update an existing reservation."""
        # Prepare update query dynamically
        update_fields = []
        params = []
        
        if name:
            update_fields.append('name = ?')
            params.append(name)
        if flight_number:
            update_fields.append('flight_number = ?')
            params.append(flight_number)
        if departure:
            update_fields.append('departure = ?')
            params.append(departure)
        if destination:
            update_fields.append('destination = ?')
            params.append(destination)
        if date:
            update_fields.append('date = ?')
            params.append(date)
        if seat_number:
            update_fields.append('seat_number = ?')
            params.append(seat_number)
        
        if not update_fields:
            return False
        
        # Add reservation ID to params
        params.append(reservation_id)
        
        try:
            # Construct and execute update query
            query = f'''
                UPDATE reservations 
                SET {', '.join(update_fields)} 
                WHERE id = ?
            '''
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_reservation(self, reservation_id):
        """Delete a reservation by its ID."""
        try:
            self.cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def close(self):
        """Close database connection."""
        self.conn.close()
