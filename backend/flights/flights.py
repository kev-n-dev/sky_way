from flask import jsonify
from datetime import datetime, timedelta
from models import Flight ,Airport

def get_flight_by_id(flight_id):
    """
    Given a flight ID, return the flight object if it exists, or None if not found.
    """
    flight = Flight.query.filter_by(id=flight_id ).first()
    return flight


def save_searched_flight(user_id, flight_id):
    """
    Save or update the search history for a user and a flight.
    If the user searches the same flight again, increment the search count.
    """
    # Check if the search already exists (user has already searched for this flight)
    existing_search = SearchHistory.query.filter_by(user_id=user_id, flight_id=flight_id).first()

    if existing_search:
        # Increment the search count if the search already exists
        existing_search.search_count += 1
        db.session.commit()  # Commit the incremented count to the database
        return existing_search
    
    # Create a new search history record if it doesn't exist
    search_history = SearchHistory(user_id=user_id, flight_id=flight_id)
    
    # Add to the session and commit
    db.session.add(search_history)
    db.session.commit()
    
    return search_history

from datetime import datetime, timedelta
from flask import jsonify

def get_close_flights(destination_airport=None, departure_airport=None, departure_date=None):
    # Initial search for exact departure date
    flights = get_all_flights(destination_airport, departure_airport, departure_date, departure_date)
    
    if flights:
        return flights , None , None 
    else:
        # Set the range for "close" dates (e.g., ±3 days)
        date_range_days = 3

        # Parse the departure date and calculate the date range
        try:
            departure_date_obj = datetime.strptime(departure_date, '%Y-%m-%d')
            start_date = departure_date_obj - timedelta(days=date_range_days)
            end_date = departure_date_obj + timedelta(days=date_range_days)
        except ValueError:
            return None, jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Search for flights within the date range
        flights = get_all_flights(destination_airport, departure_airport, start_date, end_date)
        
        if flights:
            return flights , None , None 
        return None, jsonify({"message": "No flights found close to the specified date."}), 404

    
def get_all_flights(to=None, from_airport=None, start_date=None, end_date=None):
    """
    Get a list of flights with optional filters.
    Filters are:
    - to: destination airport code (optional)
    - from_airport: departure airport code (optional)
    - start_date: start date for the flight (these are for searching flights within a range)
    - end_date: end date for the flight (these are for searching flights within a range)

    Returns a filtered list of flights based on the provided parameters.
    """
    query = Flight.query
    
    # Filter by 'to' (arrival airport)
    if to:
        query = query.filter(Flight.arrival_airport_id == Airport.query.filter(Airport.code == to).first().id)

    # Filter by 'from_airport' (departure airport)
    if from_airport:
        query = query.filter(Flight.departure_airport_id == Airport.query.filter(Airport.code == from_airport).first().id)
    
    
    if start_date is not None and start_date == end_date:
        query = query.filter(Flight.start_date == start_date)
    else:    
        # Filter by 'start_date'
        if start_date:
            query = query.filter(Flight.start_date >= start_date)
        
        # Filter by 'end_date'
        if end_date:
            query = query.filter(Flight.start_date <= end_date)
                
    # Execute the query and return the result
    flights = query.all()
    return flights



