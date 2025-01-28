from datetime import datetime
from sqlalchemy.exc import IntegrityError
from utils.users.users import get_user_by_email
from models import Booking, db, User
import uuid
from flask import jsonify, current_app 


def create_booking_entry(owner_id, departure_flight, returning_flight=None, passengers=[]):
    """
    Creates a new booking for a user, associates flights, and passengers.

    :param owner_id: ID of the user making the booking.
    :param departure_flight: ID of the departure flight.
    :param returning_flight: ID of the returning flight (nullable for one-way).
    :param passengers: List of user data dictionaries for passengers (can be empty for just the owner).
    :return: Newly created booking object or an error message.
    """
    current_app.logger.debug("Starting create_booking_entry")
    current_app.logger.debug(
        f"Parameters received: owner_id={owner_id}, departure_flight={departure_flight}, "
        f"returning_flight={returning_flight}, passengers={len(passengers)}"
    )

    try:
        # Create a new booking instance
        reference_number = str(generate_reference_number())
        booking = Booking(
            reference_number=reference_number,  # Generate a reference number
            owner_id=owner_id,  # Should be a user ID (e.g., integer or UUID)
            departure_flight_id=departure_flight,
            returning_flight_id=returning_flight,
            created_at=datetime.utcnow(),
        )
        current_app.logger.debug(f"Booking instance created with reference_number={reference_number}")

        # Process each passenger in the list
        for index, passenger in enumerate(passengers):
            current_app.logger.debug(f"Processing passenger {index + 1}/{len(passengers)}: {passenger}")

            email = passenger.get("email")
            if email:
                current_app.logger.debug(f"Looking up user by email: {email}")
                # Check if the passenger already exists
                existing_passenger = get_user_by_email(email)
                if existing_passenger:
                    current_app.logger.debug(f"Existing passenger found: {existing_passenger.email}")
                    booking.passengers.append(existing_passenger)
                else:
                    current_app.logger.debug(f"No existing passenger found for email: {email}, creating new user")

                    dob_str = passenger.get("dob")
                    dob = datetime.strptime(str(dob_str)[:10], '%Y-%m-%d').date() if dob_str else None

                    # If passenger does not exist, create a new user
                    new_user = User(
                        email=email,
                        first_name=passenger.get("first_name"),
                        last_name=passenger.get("last_name"),
                        gender=passenger.get("gender"),
                        dob=dob,
                    )
                    db.session.add(new_user)
                    db.session.flush()  # Ensure new_user ID is generated before associating
                    current_app.logger.debug(f"New user created with email: {email}")
                    booking.passengers.append(new_user)

        # Add and commit the booking to the session
        db.session.add(booking)
        db.session.commit()
        db.session.refresh(booking)
        current_app.logger.info(f"Booking successfully created with reference_number={reference_number}")

        return jsonify({"status": "success", "message": f"Booking successfully created with reference_number={reference_number}", "data": booking.to_dict()})

    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f"IntegrityError during booking creation: {e}")
        return jsonify({"status": "error", "message": "Booking creation failed due to integrity error.", "data": None})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error during booking creation: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred during booking creation.", "data": None})


def update_booking(booking_id, departure_flight_id=None, returning_flight_id=None, passengers=[]):
    """
    Update an existing booking by changing the flight or adding/removing passengers.

    :param booking_id: ID of the booking to be updated.
    :param departure_flight_id: New departure flight ID (nullable).
    :param returning_flight_id: New returning flight ID (nullable).
    :param passengers: List of user IDs for passengers to be added/removed.
    :return: Updated booking object or an error message.
    """

    current_app.logger.info("Starting update_booking function.")
    current_app.logger.debug(f"Received parameters: booking_id={booking_id}, departure_flight_id={departure_flight_id}, returning_flight_id={returning_flight_id}, passengers={passengers}")
    try:
        if not booking_id:
            current_app.logger.error("Booking ID is required but was not provided.")
            raise ValueError("Booking ID is required.")
    
        booking = Booking.query.get(booking_id)

        if not booking:
            current_app.logger.error("Booking ID is required but was not provided.")
            return jsonify({"status": "error", "message":"Booking not found.", "data": None})

    
        current_app.logger.info(f"Updating booking with ID: {booking_id}")

        if departure_flight_id:
            current_app.logger.debug(f"Updating departure flight to {departure_flight_id} for booking {booking_id}.")
            booking.departure_flight_id = departure_flight_id
        if returning_flight_id is not None:
            current_app.logger.debug(f"Updating returning flight to {returning_flight_id} for booking {booking_id}.")
            booking.returning_flight_id = returning_flight_id

        # Update passengers list
        for passenger_id in passengers:
            current_app.logger.debug(f"Updating passengers for booking {booking_id}: {passengers}.")

            user = User.query.get(passenger_id)
            if user and user not in booking.passengers:
                booking.passengers.append(user)

        db.session.commit()
        db.session.refresh(booking)
        current_app.logger.info(f"Successfully updated booking with ID: {booking_id}")
    
        return jsonify({"status": "success", "message": "Booking updated successfully", "data": booking.to_dict()})
    except Exception as e:
        current_app.logger.error(f"An error occurred while updating booking {booking_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e), "data":None})


def pay_booking(booking_id):
    """
    Process payment for a booking and mark it as completed.

    :param booking_id: ID of the booking being paid for.
    :return: Booking object with payment processed or an error message.
    """
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"status": "error", "message":  "Booking not found.", "data": None, "code": 404})


    if booking.payment_received: 
        return jsonify({"status": "error", "message":  "This booking has already been paid for.", "data": None, "code": 409})

    # Process the payment here (e.g., integrate with payment gateway)
    booking.payment_received = datetime.utcnow()
    booking.completed = datetime.utcnow()

    db.session.commit()
    db.session.refresh(booking)

    return jsonify({"status": "success", "message":  "This booking has been paid for successfully.", "data": {
        'reference_number': booking.reference_number,
        'status': 'Paid',
        'payment_received': booking.payment_received
    }, "code": 200})

def get_booking(booking_id=None, reference_number=None):
    """
    Retrieve a booking by its ID or reference number.

    :param booking_id: ID of the booking.
    :param reference_number: Reference number of the booking (nullable).
    :return: Booking object or None if not found.
    """
    current_app.logger.debug(f"starting get_booking with booking_id{booking_id}, reference_number: {reference_number}")
    try:
        if booking_id:
            booking = Booking.query.get(booking_id)  # Retrieve booking by ID
            if booking:
                return jsonify({"status": "success", "message":  "booking data successfully retrieved", "data": booking.to_dict(), "code": 200})
            else:
                current_app.logger.debug(f"booking not found from booking id {booking_id}")

        if reference_number:
            booking = Booking.query.filter_by(reference_number=reference_number).first()  # Retrieve booking by reference number
            if booking:
                return jsonify({"status": "success", "message":  "booking data successfully retrieved", "data": booking.to_dict(), "code": 200})
            else:
                current_app.logger.debug(f"booking not found from reference_number {reference_number}")

        return jsonify({"status": "error", "message":  "booking data not found" , "data": None, "code": 404})
    except Exception as e:
        current_app.logger.error(f"Error occurred in get_booking: {e}")  # Print the error for debugging
        return jsonify({"status": "error", "message":  f"booking data not found: {e}" , "data": None, "code": 500})

def generate_reference_number():
    return f"SKY-{uuid.uuid4()}"
