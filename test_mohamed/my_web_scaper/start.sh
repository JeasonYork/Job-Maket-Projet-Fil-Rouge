#!/bin/bash

# Export PATH to ensure it includes necessary directories
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/snap/bin

# Log the start time
echo "Script started at $(date)" >> /home/ubuntu/test_mohamed/my_web_scaper/debug.log

# Change to the directory where the script is located
cd /home/ubuntu/test_mohamed/my_web_scaper

# Log the current directory
echo "Current directory: $(pwd)" >> /home/ubuntu/test_mohamed/my_web_scaper/debug.log

# Build the Docker images
/snap/bin/docker-compose build

# Log after building Docker images
echo "Docker images built at $(date)" >> /home/ubuntu/test_mohamed/my_web_scaper/debug.log

# Run the Docker Compose to execute the tests
/snap/bin/docker-compose up

# Log the end time
echo "Script ended at (date)" >> /home/ubuntu/test_mohamed/my_web_scaper/debug.log
