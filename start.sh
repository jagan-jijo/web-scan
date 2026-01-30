#!/bin/bash

# Path to your virtual environment
VENV_PATH="myenv/bin/activate"

# Check if the virtual environment exists and activate it
if [ -f "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH"
else
    echo "Virtual environment not found at $VENV_PATH. Please create the virtual environment first."
    exit 1
fi


# Install necessary dependencies in the virtual environment
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Start the FastAPI server in the foreground (will shutdown if terminal closes)
echo "Starting FastAPI server..."
(
    sleep 2
    xdg-open "http://127.0.0.1:8000"
) &
uvicorn app:app --reload
