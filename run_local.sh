#!/bin/bash

# Set the virtual environment name
VENV_NAME=".venv"

# Check if the virtual environment directory exists
if [ ! -d "${VENV_NAME}" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "${VENV_NAME}"
fi

# Check if the virtual environment is activated
if [ -z "${VIRTUAL_ENV}" ]; then
    echo "Activating virtual environment..."
    source "${VENV_NAME}/bin/activate"
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Virtual environment activated."
fi

# Run the app
streamlit run app.py --server.port 8080
