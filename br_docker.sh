#!/bin/bash

# Build the Docker image
docker build -t howmyzsh .

# Run the Docker container
docker run -p 8080:8080 --name howmyzsh-container howmyzsh
