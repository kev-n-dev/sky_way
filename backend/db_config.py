from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from urllib.parse import quote_plus
from seed_data import seed_data

from models import db 


# Configuration settings
username = config.get('db-user')
password = config.get('db-password')
host = config.get('db-host')
db_name = config.get('db-name')
port = config.get('db-port') or 1433  # Default SQL Server port

 

def init_db(flask_app):    
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skyway_airlines_systems.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
    db.init_app(flask_app)
    with flask_app.app_context():
        db.drop_all()  # Drops all tables (use with caution)
        db.create_all()  # This will create all tables defined by your models
        seed_data()  # Call the seed function to load data

     