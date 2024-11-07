# Function to get a list of all airports
from models import Airport

def get_all_airports():
    """
    Get a list of all airports in the system.
    """
    airports = Airport.query.all()  # Exclude soft-deleted airports
    return [airport.to_dict() for airport in airports]

def get_airport_by_id(id):
    flight = Airport.query.filter_by(id=id).first()
    return flight

# Function to get the list of airports from all departing flights' arrival airport IDs
def get_arrival_airports_for_departing_flights(departing_airport_id):
    """
    Given an airport, get the list of arrival airports from all the departing flights' arrival_airport_id.
    """
    # Get all flights departing from the given airport
    departing_flights = Flight.query.filter_by(departure_airport_id=departing_airport_id, deleted_at=None).all()
    
    # Extract the unique arrival airports from these flights
    arrival_airports = set()
    for flight in departing_flights:
        arrival_airports.add(flight.arrival_airport)  # Add the airport object (arrival airport)

    return list(arrival_airports)
