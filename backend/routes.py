# routes.py
from flask import Blueprint, request, jsonify, current_app, abort
from models import db, Flight, Booking, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
import random
from datetime import datetime, timedelta  # Add timedelta for time manipulation
from flights.flights import get_close_flights, get_flight_by_id
from flights.airports import get_all_airports, get_airport_by_id
from bookings.booking import pay_booking, create_booking_entry, get_booking

bp = Blueprint('routes', __name__)

# Login
@bp.route('/login', methods=['POST'])
def login():
    current_app.logger.debug("Starting login process")
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        current_app.logger.error("Username or password are missing")
        abort(400, description="Email and password are required.")

    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user:
        current_app.logger.error("User not found")
        return jsonify({"message": "User not found"}), 404

    if user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        response = jsonify({"message": "Login successful.", "access_token": f'{access_token}'})
        response.headers['Authorization'] = f'Bearer {access_token}'
        return response, 200
    else:
        return jsonify({"message": "Invalid login credentials."}), 401

# Create User API
@bp.route('/register', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        abort(400, description="Name, email, and password are required.")
    
    first_name, last_name = (name.split(' ', 1) + [None])[:2]  # Split on the first space only

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists."}), 409

    new_user = User(first_name=first_name, last_name=last_name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully.", "user_id": str(new_user.id)}), 201

# Get User API
@bp.route('/get_user/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    
    if str(current_user_id) != user_id:
        return jsonify({"message": "Unauthorized access."}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify({
        "first_name": user.first_name,  
        "last_name": user.last_name,  
        "gender": user.gender,
        "email": user.email,
        "dob": user.dob,
        "created_at": user.created_at,
    }), 200

# Search Flights API
@bp.route('/search_flights', methods=['GET'])
@jwt_required()
def search_flights():
    departure_city = request.args.get('from')
    arrival_city = request.args.get('to')
    departure_date = request.args.get('depart')
    return_date = request.args.get('return')
    trip_type = request.args.get('type')
    guests = request.args.get('guests')

    current_app.logger.info(f"Search request: {departure_city}, {arrival_city}, {departure_date}, {return_date}, {trip_type}, {guests}")

    try:
        outgoing_flights, error_msg, err_code = get_close_flights(
            destination_airport=arrival_city,
            departure_airport=departure_city,
            departure_date=departure_date
        )
        
        if error_msg:
            return err_message,err_code
        returning_flights = []
        if trip_type == "Roundtrip":
            returning_flights, error_msg, err_code = get_close_flights(
                destination_airport=departure_city,
                departure_airport=arrival_city,
                departure_date=return_date
            )
            if  error_msg:
                return err_message,err_code
        response_data = {
            'outgoing_flights': [flight.to_dict() for flight in outgoing_flights],
            'returning_flights': [flight.to_dict() for flight in returning_flights] if trip_type == "Roundtrip" else []
        }
        return jsonify(response_data)
    except Exception as e:
        current_app.logger.error(f"Error processing flight search: {str(e)}")
        return jsonify({"error": "Error processing flight search"}), 500



# Create Booking API
@bp.route('/booking', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.json

    # Extract data from the request
    owner_id = get_jwt_identity()

    departing_flight = data.get('departing_flight')
    return_date = data.get('return_date')
    passengers = data.get('passengers', [])

    # Validate required fields
    if not owner_id or not departing_flight:
        return jsonify({"error": "Owner ID and Departure Flight ID are required"}), 400

    # Fetch the departure flight object
    departure_flight = get_flight_by_id(departing_flight['flight_id'])
    if not departure_flight:
        return jsonify({"error": "Invalid Departure Flight ID"}), 400

    # Handle roundtrip case and get the returning flight if specified
    returning_flight = None
    if return_date:
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
        # Find or create a return flight
        returning_flights, error_msg, err_code = get_close_flights(
            destination_airport=departure_flight.departure_airport.code,
            departure_airport=departure_flight.arrival_airport.code,
            departure_date=return_date
        )
        if returning_flights:
            returning_flight = returning_flights[0]
            print("has returning flight",returning_flights)
        else:
            print("has No returning flight creating new")
            # Convert return_date to a datetime object

            new_flight = Flight(
            id=str(uuid.uuid4()),
            flight_num=f"RF{random.randint(101, 505)}",
            departure_airport_id=departure_flight.arrival_airport.id,
            arrival_airport_id=departure_flight.departure_airport.id,
            departure_time=(datetime.combine(return_date_obj, datetime.min.time()) + timedelta(hours=1)),
            arrival_time=(datetime.combine(return_date_obj, datetime.min.time()) + timedelta(hours=3)),
            start_date=return_date_obj,  # Ensure this is a datetime.date object
            end_date=(return_date_obj + timedelta(days=1)),  # Ensure this is a datetime.date object
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
            )

            # Add to session and commit
            db.session.add(new_flight)
            db.session.commit()
            db.session.flush()
                

            returning_flight = new_flight

    # Create the booking using create_booking_entry
    booking = create_booking_entry(
        owner_id=owner_id,
        departure_flight=departure_flight.id,
        returning_flight=returning_flight.id if returning_flight else None,
        passengers=passengers
    )

    # Convert booking object to dictionary format for JSON response
    if isinstance(booking, dict) and "error" in booking:
        return jsonify(booking), 400
    
    
    return jsonify(booking.to_dict()), 201

# View Bookings API
@bp.route('/booking', methods=['GET'])
@jwt_required()
def view_bookings():
    email = request.args.get('email')
    reference_number = request.args.get('reference_number')

    if not email and not reference_number:
        return jsonify({"error": "Email or Reference Number must be provided"}), 400
    
    bookings = []
    
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        bookings = user.bookings

    if reference_number:
        booking = get_booking(None, reference_number=reference_number) 
        if booking:
            bookings.append(booking)  # Add booking to the list

    # Return the bookings in the specified format
    return jsonify([booking.to_dict() for booking in bookings]), 200

    
# Pay for Booking API
@bp.route('/booking/confirmation', methods=['POST'])
@jwt_required()
def pay_for_booking():
    data = request.json
    booking_id = data.get('booking_id')

    if not booking_id:
        return jsonify({"error": "Booking ID is required"}), 400
    return pay_booking(booking_id)

# Airports API
@bp.route('/airports', methods=['GET'])
def get_airports():
    return jsonify(get_all_airports())
