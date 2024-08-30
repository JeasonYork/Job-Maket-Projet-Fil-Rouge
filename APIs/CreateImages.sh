#!/bin/bash

# Change directory to MyDashAPI_app and build the Docker image
cd ~/APIs/MyDashAPI_app
docker build -t my-dash-app .

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Successfully built my-dash-app"
else
  echo "Failed to build my-dash-app"
  exit 1
fi

# Change directory to MyFastAPI_app and build the Docker image
cd ~/APIs/MyFastAPI_app
docker build -t my-fastapi-app .

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Successfully built my-fastapi-app"
else
  echo "Failed to build my-fastapi-app"
  exit 1
fi
