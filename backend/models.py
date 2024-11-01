# models.py
from db_config import db
from datetime import datetime

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    departure_city = db.Column(db.String(100))
    arrival_city = db.Column(db.String(100))
    date = db.Column(db.Date)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(10), unique=True)
    passenger_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
