from datetime import datetime
import bcrypt
from flask_sqlalchemy import SQLAlchemy 
import uuid

# Initialize SQLAlchemy
db = SQLAlchemy()
 
# Function to generate a default UUID
def default_uuid_generator():
    return str(uuid.uuid4())


# Define Airport Model
class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)  # Adjusted size for UUID
    code = db.Column(db.String(3))  # Airport code (e.g., 'BGI')
    name = db.Column(db.String, nullable=False)  # Full airport name (e.g., 'Barbados, Grantley Adams Int'l')

    # Define relationship to the Flight model for arriving flights
    arriving_flights = db.relationship(
        'Flight', backref='arrival_airport_ref', lazy=True,
        foreign_keys='Flight.arrival_airport_id'
    )
    # Define relationship to the Flight model for departing flights
    departing_flights = db.relationship(
        'Flight', backref='departure_airport_ref', lazy=True,
        foreign_keys='Flight.departure_airport_id'
    )
    def __repr__(self):
        return f"Airport(code={self.code}, name={self.name})"

    def get_arriving_flights(self):
        """
        Get a list of all flights arriving at this airport.
        """
        return self.arriving_flights

    def get_departing_flights(self):
        """
        Get a list of all flights departing from this airport.
        """
        return self.departing_flights

    
# Define Flight model
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)
    flight_num = db.Column(db.String(10), unique=True, nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False)
    arrival_time = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
      
 
    def __repr__(self):
        return f'<Flight {self.flight_num} from {self.departure_airport_ref.name} to {self.arrival_airport_ref.name}>'

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)  # Adjusted size for UUID
    password_hash = db.Column(db.String(128))  # Store hashed password
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)  # Ensure email uniqueness
    dob = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to set hashed password
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to verify password
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def full_name(self):
        return f'{first_name} {last_name}'
    def get_bookings(self):
        """
        Retrieve all bookings associated with the user,
        whether the user is the owner or one of the passengers.
        """
        # Get bookings where the user is the owner
        # owner_bookings = Booking.query.filter_by(owner_id=self.id).all()

        # Get bookings where the user is a passenger (in a many-to-many relationship)
        passenger_bookings = Booking.query.join(booking_passenger).filter(booking_passenger.c.user_id == self.id).all()

        # Combine both lists (owner_bookings + passenger_bookings) and return
        return passenger_bookings
            
booking_passenger = db.Table(
    'booking_passenger',
    db.Column('booking_id', db.String(36), db.ForeignKey('bookings.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True)
)
# Define Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)  # Adjusted size for UUID
    reference_number = db.Column(db.String(10), unique=True)
    flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'))  # Match primary key type for flights
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'))      # Match primary key type for users
    departure_flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'), nullable=False)  # Foreign key to Departure flight
    returning_flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'), nullable=True)  # Foreign key to Returning flight (nullable for one-way)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to User (owner)
    owner = db.relationship('User', backref='bookings')
    
    # Relationship to Flight (departure flight)
    departure_flight = db.relationship('Flight', foreign_keys=[departure_flight_id], backref='departure_bookings')

    # Relationship to Flight (returning flight)
    returning_flight = db.relationship('Flight', foreign_keys=[returning_flight_id], backref='returning_bookings')

    # Many-to-many relationship with passengers (users)
    # Define relationship with User model
    passengers = db.relationship(
        'User',
        secondary=booking_passenger,  # Ensure booking_passenger table is defined
        backref='user_bookings'  # Use a unique backref name here
    )
    
    
    def __repr__(self):
        return f"<Booking reference_number={self.reference_number}, owner={self.owner.full_name()}, passengers={len(self.passengers)}>"

    def is_round_trip(self):
        """
        Returns True if the booking is a round-trip, else False.
        """
        return self.returning_flight_id is not None
    
    
    def get_trip_status(self):
        """
        Get the status of the trip: 'current', 'future', or 'past'.
        """
        # Get the flight's start date
        flight_date = self.flight.start_date

        # Get today's date
        today = datetime.utcnow().date()

        # Compare the flight's date with today's date
        if flight_date > today:
            return "future"
        elif flight_date == today:
            return "current"
        else:
            return "past"
        
        
        
        
        
        
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'), nullable=False)  # Foreign key to Flight
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for search
    search_count = db.Column(db.Integer, default=1)  # Counter for the number of times this user searched for this flight

    user = db.relationship('User', backref='search_history', lazy=True)
    flight = db.relationship('Flight', backref='search_history', lazy=True)

    def __repr__(self):
        return f"SearchHistory(user_id={self.user_id}, flight_id={self.flight_id}, searched_at={self.searched_at})"
