import sqlite3

class FlightDatabase:
    def __init__(self, db_name='flight_reservations.db'):
        """Initialize database connection and create tables if not exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables for flight reservations."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                flight_id INTEGER PRIMARY KEY,
                flight_number TEXT UNIQUE,
                origin TEXT,
                destination TEXT,
                departure_time TEXT,
                total_seats INTEGER,
                available_seats INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY,
                flight_id INTEGER,
                passenger_name TEXT,
                passenger_email TEXT,
                seat_number TEXT,
                FOREIGN KEY (flight_id) REFERENCES flights (flight_id)
            )
        ''')
        self.conn.commit()

    def add_flight(self, flight_number, origin, destination, departure_time, total_seats):
        """Add a new flight to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO flights 
                (flight_number, origin, destination, departure_time, total_seats, available_seats) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (flight_number, origin, destination, departure_time, total_seats, total_seats))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_available_flights(self):
        """Retrieve all available flights with seats."""
        self.cursor.execute('''
            SELECT * FROM flights WHERE available_seats > 0
        ''')
        return self.cursor.fetchall()

    def make_reservation(self, flight_id, passenger_name, passenger_email):
        """Make a reservation for a flight."""
        try:
            # Check if flight exists and has available seats
            self.cursor.execute('SELECT available_seats FROM flights WHERE flight_id = ?', (flight_id,))
            available_seats = self.cursor.fetchone()
            
            if not available_seats or available_seats[0] <= 0:
                return False

            # Insert reservation
            self.cursor.execute('''
                INSERT INTO reservations 
                (flight_id, passenger_name, passenger_email, seat_number) 
                VALUES (?, ?, ?, ?)
            ''', (flight_id, passenger_name, passenger_email, f'SEAT-{available_seats[0]}'))

            # Update available seats
            self.cursor.execute('''
                UPDATE flights 
                SET available_seats = available_seats - 1 
                WHERE flight_id = ?
            ''', (flight_id,))
            
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def close(self):
        """Close database connection."""
        self.conn.close()
