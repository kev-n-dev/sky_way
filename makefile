# Define variables
ANGULAR_PROJECT_DIR = ./frontend/skyway_frontend
FLASK_APP_DIR = ./backend
STATIC_DIR = $(FLASK_APP_DIR)/static/skyway_frontend
VENV_DIR = venv  # Directory for the virtual environment

# Targets
.PHONY: all build serve clean install setup-venv

all: setup-venv install build serve

setup-venv:
	@echo "Setting up virtual environment..."
	@python3 -m venv $(VENV_DIR)  # Create a virtual environment
	@echo "Virtual environment created. To activate it, run:"
	@echo "  source venv/bin/activate"

install:
	@echo "Installing Flask and dependencies..."
	@venv/bin/pip install -r requirements.txt
	@echo "Checking if Angular CLI is installed..."
	@if ! command -v ng &> /dev/null; then \
		echo "Angular CLI not found. Installing Angular CLI..."; \
		npm install -g @angular/cli; \
	else \
		echo "Angular CLI already installed."; \
	fi
	@echo "Building Angular project..."
	cd $(ANGULAR_PROJECT_DIR) && ng build --configuration production
	@echo "Copying built files to Flask static directory..."
	mkdir -p $(STATIC_DIR)
	cp -r $(ANGULAR_PROJECT_DIR)/dist/skyway_frontend/* $(STATIC_DIR)/
	@echo "finished copying"
 
setup:
	docker-compose up -d redis rds


serve:
	@echo "Starting Flask server..."  # Print a message indicating the start of the Flask server
	@echo "Looking for app directory: $(FLASK_APP_DIR)"
	@echo "Waiting for the database to start..."
	@FLASK_APP=$(FLASK_APP_DIR)/app.py venv/bin/flask run  # Run Flask directly from the virtual environment

clean:
	@echo "Cleaning up..."
	rm -rf $(STATIC_DIR)/*
