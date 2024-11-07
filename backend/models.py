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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }

    def __repr__(self):
        return f'<Airport {self.code}: {self.name} >'
    
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

    # Relationships to Airport model with explicit names
    departure_airport = db.relationship(
        "Airport",
        foreign_keys=[departure_airport_id],
        backref=db.backref("flights_departing", lazy="dynamic")
    )
    arrival_airport = db.relationship(
        "Airport",
        foreign_keys=[arrival_airport_id],
        backref=db.backref("flights_arriving", lazy="dynamic")
    )
    
    def duration(self):
        try:
            # Combine the start_date and departure_time into a single datetime object
            departure_datetime = datetime.combine(self.start_date, datetime.strptime(self.departure_time, '%I:%M %p').time())
            arrival_datetime = datetime.combine(self.end_date, datetime.strptime(self.arrival_time, '%I:%M %p').time())
        
            # Calculate the duration of the flight in hours
            duration = (arrival_datetime - departure_datetime).total_seconds() / 3600  # duration in hours
 
            
            return round(duration, 1)  # Rounded to two decimal places, or use {:.2g} for significant figures
            
        
        
        except Exception as e:
            arrival_time = datetime.strptime(self.arrival_time, "%Y-%m-%d %H:%M:%S")
            departure_time = datetime.strptime(self.departure_time, "%Y-%m-%d %H:%M:%S")

            # Calculate the difference between the two datetime objects
            time_difference = arrival_time - departure_time
            difference_in_hours = time_difference.total_seconds() / 3600

            return difference_in_hours 
        
    
    def cost(self):
        try:
            # Calculate the cost (cost per hour = $180)
            cost = self.duration() * 47
            
            # Return the cost as a formatted string with a dollar sign
            return f'${cost:.2f}'
        
        except Exception as e:
            cost = 12 * 47
            return f'${cost:.2f}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'flight_num': self.flight_num,
            'departure_airport': self.departure_airport.to_dict() if self.departure_airport else None,
            'arrival_airport': self.arrival_airport.to_dict() if self.arrival_airport else None,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'cost': self.cost(),
            'duration':self.duration(),
        }

    def __repr__(self):
        return f'<Flight {self.flight_num} from {self.departure_airport.name} to {self.arrival_airport.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    dob = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to set hashed password
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to verify password
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_bookings(self):
        # Retrieve all bookings associated with the user
        passenger_bookings = Booking.query.join(booking_passenger).filter(booking_passenger.c.user_id == self.id).all()
        return passenger_bookings

    def to_dict(self):
        """
        Converts the User instance to a dictionary format.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "email": self.email,
            "dob": self.dob.isoformat() if self.dob else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "full_name": self.full_name()
        }

         
         
booking_passenger = db.Table(
    'booking_passenger',
    db.Column('booking_id', db.String(36), db.ForeignKey('bookings.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True)
)
# Define Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.String(36), primary_key=True, default=default_uuid_generator)
    reference_number = db.Column(db.String(10), unique=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    departure_flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'), nullable=False)
    returning_flight_id = db.Column(db.String(36), db.ForeignKey('flights.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.DateTime)
    payment_received = db.Column(db.DateTime)

    owner = db.relationship('User', backref='bookings')
    departure_flight = db.relationship('Flight', foreign_keys=[departure_flight_id], backref='departure_bookings')
    returning_flight = db.relationship('Flight', foreign_keys=[returning_flight_id], backref='returning_bookings')
    passengers = db.relationship('User', secondary=booking_passenger, backref='user_bookings')

    def __repr__(self):
        return f"<Booking reference_number={self.reference_number}, owner={self.owner.full_name()}, passengers={len(self.passengers)}>"

    def is_round_trip(self):
        return self.returning_flight_id is not None

    def get_trip_status(self):
        flight_date = self.departure_flight.start_date if self.departure_flight else None
        today = datetime.utcnow().date()
        if flight_date:
            if flight_date > today:
                return "future"
            elif flight_date == today:
                return "current"
            else:
                return "past"
        return "unknown"

    def to_dict(self):
        return {
            "id": self.id,
            "reference_number": self.reference_number,
            "owner": self.owner.to_dict() if self.owner else None,  # Ensure User model has `to_dict`
            "departure_flight": self.departure_flight.to_dict() if self.departure_flight else None,
            "returning_flight": self.returning_flight.to_dict() if self.returning_flight else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed": self.completed.isoformat() if self.completed else None,
            "payment_received": self.payment_received.isoformat() if self.payment_received else None,
            "is_round_trip": self.is_round_trip(),
            "trip_status": self.get_trip_status(),
            "passengers": [p.to_dict() for p in self.passengers]  # Ensure User model has `to_dict`
        }

        
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
