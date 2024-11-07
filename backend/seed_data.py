import os
import json
from datetime import datetime, timedelta
import itertools
import uuid
from models import db, Flight, Airport  # Ensure you have imported your models
import random

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



 
 

from datetime import datetime, timedelta
import random
import uuid
import itertools

def add_flight_data_to_db(airports):
    """
    Generate and insert flight data for all unique combinations of airports.

    :param airports: List of airport records from the database, each with an 'id' and 'code'.
    """
    flight_num_counter = 101  # Starting flight number
    
    # Generate all unique airport code pairs
    airport_pairs = list(itertools.permutations(airports, 2))
    
    for from_airport, to_airport in airport_pairs:
        # Generate a random time between 6:00 AM and 9:00 PM for departure (in 24-hour format)
        random_hour = random.randint(6, 21)  # Random hour between 6 AM and 9 PM
        random_minute = random.randint(0, 59)  # Random minute between 0 and 59
        
        # Adjust for 12-hour format (e.g., 0:00 to 12:00 AM)
        if random_hour == 12:
            hour_12 = 12
            am_pm = 'PM'
        elif random_hour > 12:
            hour_12 = random_hour - 12
            am_pm = 'PM'
        else:
            hour_12 = random_hour
            am_pm = 'AM'

        # Construct the time in 12-hour format (e.g., '06:45 AM')
        departure_time_str = f"{hour_12:02d}:{random_minute:02d} {am_pm}"

        # Convert to a datetime object using the correct format for 12-hour time with AM/PM
        try:
            departure_time = datetime.strptime(departure_time_str, "%I:%M %p")
        except ValueError as ve:
            print(f"Error parsing time '{departure_time_str}': {ve}")
            continue  # Skip to the next flight if there's an error in time format

        # Generate a random flight duration between 30 minutes (0.5 hours) and 3 hours
        flight_duration_minutes = random.randint(55, 180)  # Random duration in minutes
        flight_duration = timedelta(minutes=flight_duration_minutes)

        # Calculate arrival time by adding the random duration to the departure time
        arrival_time = departure_time + flight_duration
        
        
            
        # Generate a random start date in the future (after today's date)
        today = datetime.utcnow()
        random_days_ahead = random.randint(1, 365)  # Random number of days in the future (1 to 365)
        start_date = today + timedelta(days=random_days_ahead)

        
        added_days = random.randint(1, 2)
        
        if arrival_time < departure_time and added_days < 1:
            added_days =1
        # Generate a random end date (ensure it is after the start date)
        end_date = start_date + timedelta(days=added_days)  # Random end date within 1 to 30 days after start date

         
        # Create a new Flight entry
        new_flight = Flight(
            id=str(uuid.uuid4()),
            flight_num=f"BW{flight_num_counter}",
            departure_airport_id=from_airport.id,
            arrival_airport_id=to_airport.id,
            departure_time=departure_time.strftime("%I:%M %p"),  # Format as 12-hour time with AM/PM
            arrival_time=arrival_time.strftime("%I:%M %p"),
            start_date=start_date,
            end_date=end_date,
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
