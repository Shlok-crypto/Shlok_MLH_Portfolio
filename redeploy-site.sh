#!/bin/bash

# Script: redeploy-site.sh
# Description: Automates the redeployment of the Flask portfolio site on the VPS.
# This script should be run after SSHing into the VPS.

# Exit immediately if a command exits with a non-zero status.
# This ensures that the script stops if any command fails (e.g., git pull fails, pip install fails).
set -e

# --- Configuration ---
# Define the absolute path to your Flask project directory on the VPS.
# Based on our previous conversation, it's likely in /root/Shlok_MLH_Portfolio
PROJECT_DIR="/root/Shlok_MLH_Portfolio"

# This is the service that will be restarted after updates.
FLASK_SERVICE_NAME="myportfolio"

echo "Starting redeployment process for the Flask portfolio site..."
echo "------------------------------------------------------------"

# Step 1: Change into your project folder
echo "1. Navigating to project directory: {$PROJECT_DIR}"
cd "${PROJECT_DIR}"

# Step 2: Run git fetch && git reset origin/main --hard
echo "Fetching and resetting git repository to origin/main..."
git fetch && git reset origin/main --hard || { echo "Error: Git operations failed. Exiting."; exit 1; }

# Step 3: Enter the python virtual environment and Install python dependencies.
echo "3. Activating Python virtual environment and installing/updating dependencies..."
source .venv/bin/activate

# 'pip install -r requirements.txt' installs or updates all Python packages
pip install -r requirements.txt
echo "Python dependencies installed/updated."

# Step 4: Restart myportfolio service.
echo "4. Restarting the '$FLASK_SERVICE_NAME' systemd service..."

systemctl start "$FLASK_SERVICE_NAME"
systemctl enable "$FLASK_SERVICE_NAME"
echo "Service '$FLASK_SERVICE_NAME' restarted successfully."

echo "------------------------------------------------------------"
echo "Redeployment process complete. Your site should now be live"
