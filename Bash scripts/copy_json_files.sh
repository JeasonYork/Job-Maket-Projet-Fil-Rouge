#!/bin/bash

# Local directory containing JSON files
LOCAL_DIR="D:/DataScientest/Projects/my-project/Scripts/Data_Job_10-05-2023"

# Remote directory on the VM
REMOTE_DIR="test_said"

# SSH command to connect to the VM
SSH_CMD="ssh -i /C:/Users/csaid/.ssh/oct23_cde_job-market.pem ubuntu@13.51.121.165"

# Loop through each JSON file in the local directory and copy it to the remote directory
for file in "$LOCAL_DIR"/*.json; do
    # Extract the filename from the full path
    filename=$(basename "$file")
    
    # Copy the JSON file to the VM using SCP
    scp -i /mnt/c/Users/csaid/.ssh/oct23_cde_job-market.pem "$file" ubuntu@13.51.121.165:"$REMOTE_DIR"/"$filename"
    
    # Optionally, you can print a message for each file copied
    echo "Copied $filename to VM"
done

# Optionally, you can add a message to indicate when all files have been copied
echo "All JSON files copied to the VM"
