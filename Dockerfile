# Use recent Python image
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Update package lists, install necessary dependencies, and build dependencies for duckdb and hnswlib
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgomp1 && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the GIT_PYTHON_GIT_EXECUTABLE environment variable
ENV GIT_PYTHON_GIT_EXECUTABLE /usr/bin/git

# Expose the port the app will run on
EXPOSE 8080

# Define the entrypoint command
CMD ["streamlit", "run", "app.py", "--server.port=8080"]
