#!/bin/bash

# Set your project ID, service name, and image name
PROJECT_ID="your_project_id"
SERVICE_NAME="myapp"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Authenticate with gcloud CLI
gcloud auth login

# Set the project and compute zone
gcloud config set project ${PROJECT_ID}
gcloud config set compute/zone <your_compute_zone>

# Build the Docker image
docker build -t ${IMAGE_NAME} .

# Push the Docker image to Google Container Registry
docker push ${IMAGE_NAME}

# Deploy the app on Google Cloud Run
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region <your_region> \
    --allow-unauthenticated
