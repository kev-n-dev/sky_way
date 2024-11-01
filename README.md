
# SkyWay Project

SkyWay is a web application using Angular for the frontend and Flask for the backend. The frontend is built and served as static files through Flask, allowing for client-side Angular routing and a backend API.

## Project Structure

```plaintext
sky_way/
├── backend/                    # Flask backend and API
│   ├── app.py                  # Main Flask application
│   ├── db_config.py            # Database configuration
│   └── static/                 # Angular build directory served by Flask
│       └── skyway_frontend/
├── frontend/
│   └── skyway_frontend/        # Angular frontend project
├── Makefile                    # Makefile with setup and run commands
└── README.md                   # Project instructions
```

## Prerequisites

1. **Python 3.12+**: Ensure Python is installed and accessible.
2. **Node.js & npm**: Required for building the Angular frontend.
3. **Angular CLI**: Installed globally (`npm install -g @angular/cli`).

## Initial Setup

To set up and run the project, follow these steps:

### 1. Clone the Repository

```bash
git clone <repo_url>
cd sky_way
```

### 2. Set Up the Virtual Environment

The project uses a virtual environment to manage dependencies. Run the following command to create and activate the virtual environment:

```bash
make setup-venv
```

This command will:
- Create a virtual environment in the `venv` folder.
- Activate the virtual environment.

### 3. Install Backend Dependencies

With the virtual environment active, install Flask and any other required Python packages:

```bash
make install
```

### 4. Build the Angular Frontend

Build the Angular project and copy the static files to the Flask `static` directory:

```bash
make build
```

This command will:
- Build the Angular project using the `production` configuration.
- Copy the built files into the Flask `static/skyway_frontend` directory.

### 5. Serve the Application

Run the Flask server with the following command:

```bash
make serve
```

The server will start on `http://127.0.0.1:5000` and serve both the backend API and the Angular frontend.

### 6. Cleaning Up

To remove all built static files:

```bash
make clean
```

## Additional Information

### Routes

- **`/api/*`**: Reserved for backend API routes.
- **All other routes**: Served by the Angular frontend (uses Angular routing).

### Common Issues

- **Python or pip not found**: Ensure Python 3.12+ is installed and correctly added to your PATH.
- **`make setup-venv` errors**: Run `source venv/bin/activate` manually if necessary.
- **404 Errors**: Verify that Angular build files are correctly placed in the `backend/static/skyway_frontend` directory.

## License

This project is licensed under the MIT License.
