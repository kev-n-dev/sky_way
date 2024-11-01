# routes.py
from flask import Blueprint, request, jsonify
from models import db, Flight, Booking
import uuid

bp = Blueprint('routes', __name__)

# Search Flights API
@bp.route('/api/search_flights', methods=['GET'])
def search_flights():
    departure_city = request.args.get('departure_city')
    arrival_city = request.args.get('arrival_city')
    date = request.args.get('date')

    flights = Flight.query.filter_by(
        departure_city=departure_city,
        arrival_city=arrival_city,
        date=date
    ).all()
    return jsonify([{'id': f.id, 'departure_city': f.departure_city, 'arrival_city': f.arrival_city, 'date': f.date} for f in flights])

# Create Booking API
@bp.route('/api/create_booking', methods=['POST'])
def create_booking():
    data = request.json
    flight_id = data.get('flight_id')
    passenger_name = data.get('passenger_name')
    email = data.get('email')

    # Generate a unique reference number
    reference_number = str(uuid.uuid4())[:8].upper()

    booking = Booking(reference_number=reference_number, passenger_name=passenger_name, email=email, flight_id=flight_id)
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'reference_number': reference_number})

# View Bookings API
@bp.route('/api/view_bookings', methods=['GET'])
def view_bookings():
    email = request.args.get('email')
    reference_number = request.args.get('reference_number')
    last_name = request.args.get('last_name')

    bookings = Booking.query.filter_by(email=email, reference_number=reference_number).all()
    return jsonify([{'reference_number': b.reference_number, 'passenger_name': b.passenger_name, 'email': b.email} for b in bookings])
