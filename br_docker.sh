#!/bin/bash

# Build and run the Docker container for the HowMyZsh project
docker build -t howmyzsh .
docker run -p 8080:8080 --name howmyzsh-container howmyzsh
