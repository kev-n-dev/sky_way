# routes.py
from flask import Blueprint, request, jsonify, current_app
from models import db, Flight, Booking, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid


bp = Blueprint('routes', __name__)

 # Login
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Email and password are required.")

    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
        # Create a new access token
        access_token = create_access_token(identity=user.id)

        # Return the access token in the response header as Bearer token
        response = jsonify({"message": "Login successful."})
        response.headers['Authorization'] = f'Bearer {access_token}'
        
        return response, 200
    else:
        return jsonify({"message": "Invalid email or password."}), 401
    
    
# Create User API
@bp.route('/register', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        abort(400, description="Name, email, and password are required.")

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists."}), 409

    # Create and save the new user
    new_user = User(name=name, email=email)
    new_user.set_password(password)  # Hash and set the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully.", "user_id": str(new_user.id)}), 201

# Get User API
@bp.route('/get_user/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    print(user_id)
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    # Return user details without the password hash
    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }), 200



# Search Flights API
@bp.route('/search_flights', methods=['GET'])
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
