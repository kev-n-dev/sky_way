
---

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

### 4. Serve the Application

Run the Flask server with the following command:

```bash
make serve
```

The server will start on `http://127.0.0.1:5000` and serve both the backend API and the Angular frontend.

### 5. Cleaning Up

To remove all built static files:

```bash
make clean
```

## Routes and JWT Authentication

### Public Routes (No JWT Required)
- **Login Route (`/login`)**  
  Method: `POST`  
  Description: Handles user login by validating email and password. Returns a JWT access token for successful login.

- **Create User Route (`/register`)**  
  Method: `POST`  
  Description: Registers a new user with a name, email, and password.

- **Airports Route (`/airports`)**  
  Method: `GET`  
  Description: Returns a list of all available airports.

### Protected Routes (JWT Required)
These routes require a valid JWT token to be included in the `Authorization` header as a Bearer token.

- **Get User Route (`/get_user/<user_id>`)**  
  Method: `GET`  
  Description: Retrieves user details (first name, last name, gender, etc.).  
  JWT: Required (access restricted to the logged-in user only).

- **Search Flights Route (`/search_flights`)**  
  Method: `GET`  
  Description: Searches for flights based on provided criteria (departure city, arrival city, dates, etc.).  
  JWT: Required.

- **Create Booking Route (`/booking`)**  
  Method: `POST`  
  Description: Creates a new booking with departing flight, return date, and passengers.  
  JWT: Required.

- **View Bookings Route (`/booking`)**  
  Method: `GET`  
  Description: Views bookings based on email or reference number.  
  JWT: Required.

- **Pay for Booking Route (`/booking/confirmation`)**  
  Method: `POST`  
  Description: Processes payment for a booking.  
  JWT: Required.

### Example of Accessing Protected Routes

To access the protected routes, include the JWT token in the `Authorization` header as a Bearer token. Here’s an example of how to make a request using `curl`:

```bash
curl -X GET "http://127.0.0.1:5000/search_flights?from=New%20York&to=Los%20Angeles" \
-H "Authorization: Bearer <your_jwt_token>"
```

### Common Issues

- **Python or pip not found**: Ensure Python 3.12+ is installed and correctly added to your PATH.
- **`make setup-venv` errors**: Run `source venv/bin/activate` manually if necessary.
- **404 Errors**: Verify that Angular build files are correctly placed in the `backend/static/skyway_frontend` directory.

## License
This project is licensed under the [Proprietary License](LICENSE).
You may not use this software for commercial purposes without explicit permission from the author. 