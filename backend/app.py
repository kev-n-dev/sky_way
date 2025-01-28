import logging
from flask import Flask, send_from_directory, jsonify, abort, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from routes import bp  # Import blueprint for routing
from db_config import init_db  # Initialize database config

# Initialize the Flask app
app = Flask(__name__, static_folder='static/skyway_frontend/browser', static_url_path='/static')
app.config['LOG_LEVEL'] = 'DEBUG'  # Logging level
app.config["DEBUG"] = True  # Enable debug mode
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Secret key for JWT token signing
app.config['SECRET_KEY'] = 'your-flask-secret-key'  # Secret key for Flask session management

    # Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG
logger = logging.getLogger('werkzeug')  # Grab the Flask/Werkzeug logger
logger.setLevel(logging.DEBUG)

# Optionally add a custom log format
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] in %(module)s: %(message)s'
)
for handler in logger.handlers:
    handler.setFormatter(formatter)

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logging.DEBUG)


    
# Initialize the database
init_db(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Set up the JWT Manager
jwt = JWTManager(app)

# Register the blueprint for API routes
app.register_blueprint(bp, url_prefix='/api')

# Define the base route to serve the Angular app's 'index.csr.html'
@app.route('/')
def serve_index():
    """
    Serve the Angular app's index page for the base route.
    """
    return send_from_directory(app.static_folder, 'index.csr.html')

# Catch all non-API routes and redirect them to Angular's 'index.csr.html'
@app.route('/<path:path>')
def serve_path(path=None):
    """
    Serve the Angular index page for any path that doesn't match API routes.
    Excludes API paths and serves 'index.csr.html' for others like '/sw/*'.
    """
    if path and path.startswith('api/'):
        return "Not found", 404  # Return 404 for API routes
    if path and path.startswith('sw/'):
        return send_from_directory(app.static_folder, 'index.csr.html')
    return send_from_directory(app.static_folder, path)

# Serve static files from the 'static' folder, excluding API paths
@app.route('/static/<path:path>')
def serve_static(path):
    """
    Serve static files (images, JS, CSS, etc.) from the 'static' folder.
    """
    return send_from_directory(app.static_folder, path)

# Configure logging
def configure_logging(app):
    """
    Configure logging for the Flask application.
    """
    handler = logging.StreamHandler()  # Logs to stderr
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to Flask's app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL'], logging.DEBUG))  # Use the log level from config

# Run the Flask app in debug mode for development purposes
if __name__ == '__main__':
    configure_logging(app)
    app.run(debug=True)
