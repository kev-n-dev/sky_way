from flask import Flask, send_from_directory
# Import your database initialization function and blueprint
# from your_module import init_db, bp

from db_config import init_db
from routes import bp


app = Flask(__name__, static_folder='static/skyway_frontend/browser')
init_db(app)
app.register_blueprint(bp)

# Serve Angular index.html for the base route


app = Flask(__name__, static_folder='static/skyway_frontend/browser')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.csr.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)

