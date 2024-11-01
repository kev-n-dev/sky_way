# db_config.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'  # Change to SQL Server URI if needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)