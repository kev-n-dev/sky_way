# app.py
from flask import Flask, send_from_directory
from db_config import init_db
from routes import bp

app = Flask(__name__, static_folder='static/skyway_frontend/browser')
init_db(app)
app.register_blueprint(bp)

# Serve Angular index.html for the base route
@app.route('/')
@app.route('/<path:path>')
def serve_angular(path=''):
    if path != "" and path != "index.html" and path.startswith("api/"):
        return app.send_static_file(path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
