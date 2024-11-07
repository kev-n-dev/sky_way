from flask import Flask, send_from_directory, jsonify, abort
from flask_cors import CORS
from routes import bp
from flask_sqlalchemy import SQLAlchemy
from db_config import init_db
from flask_jwt_extended import JWTManager

# Initialize the Flask app once
app = Flask(__name__, static_folder='static/skyway_frontend/browser', static_url_path='/static')
init_db(app)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
app.config['SECRET_KEY'] = 'your-flask-secret-key'


# Register the API blueprint with a prefix
app.register_blueprint(bp, url_prefix='/api')

# Define the paths that should redirect to index.csr.html
 


    
    
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.csr.html')

# Serve Angular index.csr.html for the base route and other specified paths
@app.route('/<path:path>')  # Catch all routes that are not API
def serve_path(path=None):
    if path and path.startswith('api/'):  # Exclude API paths from this handling
        return "Not found", 404
    if path and path.startswith('sw/'):  # Check if path matches any of the redirect paths
        return send_from_directory(app.static_folder, 'index.csr.html')
    return send_from_directory(app.static_folder, path)

# Serve static files, excluding API paths
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)



 
if __name__ == '__main__':
    app.run(debug=True)
