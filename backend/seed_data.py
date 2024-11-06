import os
import json
from datetime import datetime, timedelta
import itertools
import uuid
from models import db, Flight, Airport  # Ensure you have imported your models

from sqlalchemy.exc import IntegrityError

def load_airports_from_json(json_file_path):
    # Ensure the correct relative path is used
    json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'airports.json')
    
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data




def seed_data():
 
    #  airports
    # Load airport data from the JSON file
    airports_data = load_airports_from_json('airports.json')
    # Call the function to insert airports into the database
    create_airports(airports_data)  
    # Retrieve airports from the database
    airports = Airport.query.all()
    add_flight_data_to_db(airports)
    
    
     
     
     
def create_airports(entries):
    """
    Function to insert airport entries into the database.

    :param entries: List of dictionaries containing airport data.
    :return: None
    """
    for airport in entries:
        try:
            # Create a new Airport object for each entry
            new_airport = Airport(code=airport['code'], name=airport['name'])
            
            # Add the new airport object to the session
            db.session.add(new_airport)
        
        except IntegrityError as e:
            # Handle cases where the airport code already exists
            print(f"Error inserting airport with code {airport['code']}: {e.orig}")
    
    try:
        # Commit all entries to the database
        db.session.commit()
        print(f"Successfully inserted {len(entries)} airports into the database.")
    except Exception as e:
        # Rollback in case of any errors during commit
        db.session.rollback()
        print(f"Error committing to the database: {e}")


def add_flight_data_to_db(airports):
    """
    Generate and insert flight data for all unique combinations of airports.

    :param airports: List of airport records from the database, each with an 'id' and 'code'.
    """
    flight_num_counter = 101  # Starting flight number
    
    # Generate all unique airport code pairs
    airport_pairs = list(itertools.permutations(airports, 2))
    
    for from_airport, to_airport in airport_pairs:
        # Generate flight times with slight variations
        departure_time = datetime.strptime("08:00 AM", "%I:%M %p") + timedelta(hours=flight_num_counter % 10)
        arrival_time = departure_time + timedelta(hours=1, minutes=30)  # Assuming 1.5 hours flight duration

        # Create a new Flight entry
        new_flight = Flight(
            id=str(uuid.uuid4()),
            flight_num=f"BW{flight_num_counter}",
            departure_airport_id=from_airport.id,
            arrival_airport_id=to_airport.id,
            departure_time=departure_time.strftime("%I:%M %p"),
            arrival_time=arrival_time.strftime("%I:%M %p"),
            start_date=datetime(2024, 11, 7),
            end_date=datetime(2025, 10, 30),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add and commit the new flight object to the session
        db.session.add(new_flight)
        flight_num_counter += 1

    try:
        # Commit all entries to the database
        db.session.commit()
        print(f"Successfully inserted {flight_num_counter - 101} flights into the database.")
    except Exception as e:
        # Rollback in case of any errors during commit
        db.session.rollback()
        print(f"Error committing flights to the database: {e}")


