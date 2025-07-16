#!/usr/bin/env bash

# redeploy-site.sh
# This script automates the deployment process for a Flask application on a VPS.
# It kills existing tmux sessions, updates the git repository,
# installs Python dependencies, and starts the Flask server in a new detached tmux session.

# --- Configuration ---
# IMPORTANT: Replace this with the actual path to your Flask project directory on the VPS.
PROJECT_DIR="/root/Shlok_MLH_Portfolio"
# Name for the new tmux session
TMUX_SESSION_NAME="flask_server"

# Name of your Python virtual environment directory within the project
VENV_DIR="venv"

# Command to start your Flask application
# "python app.py" or "python -m flask run --host=0.0.0.0"
FLASK_START_COMMAND="flask run --host=0.0.0.0"

# --- Script Logic ---

echo "Starting redeployment process..."

# 1. Kill all existing tmux sessions to ensure no old Flask servers are running
echo "Killing all existing tmux sessions..."
tmux kill-server &>/dev/null || echo "No active tmux sessions found to kill."

# 2. Change into the project directory
echo "Navigating to project directory: ${PROJECT_DIR}"
cd "${PROJECT_DIR}" || { echo "Error: Project directory not found at ${PROJECT_DIR}. Exiting."; exit 1; }

# 3. Pull latest changes from git
echo "Fetching and resetting git repository to origin/main..."
git fetch && git reset origin/main --hard || { echo "Error: Git operations failed. Exiting."; exit 1; }

# 4. Enter the Python virtual environment and install dependencies
echo "Activating virtual environment and installing Python dependencies..."
# Check if virtual environment exists
if [ -d "${VENV_DIR}" ]; then
  source "${VENV_DIR}/bin/activate" || { echo "Error: Failed to activate virtual environment. Exiting."; exit 1; }
  pip install -r requirements.txt || { echo "Error: Failed to install Python dependencies. Exiting."; exit 1; }
else
  echo "Warning: Virtual environment '${VENV_DIR}' not found. Skipping activation and dependency installation."
  echo "Please ensure your virtual environment is set up correctly."
fi

# 5. Start a new detached Tmux session and run the Flask server
echo "Starting new detached tmux session '${TMUX_SESSION_NAME}'..."

# Check if the virtual environment is active before attempting to run Flask in tmux
if command -v deactivate &>/dev/null; then
  # Create a new detached tmux session
  tmux new-session -d -s "${TMUX_SESSION_NAME}"

  # Send commands to the new tmux session
  # Change directory inside tmux
  tmux send-keys -t "${TMUX_SESSION_NAME}" "cd ${PROJECT_DIR}" C-m
  # Activate virtual environment inside tmux
  tmux send-keys -t "${TMUX_SESSION_NAME}" "source ${VENV_DIR}/bin/activate" C-m
  # Start Flask server inside tmux
  tmux send-keys -t "${TMUX_SESSION_NAME}" "${FLASK_START_COMMAND}" C-m

  echo "Flask server started in tmux session '${TMUX_SESSION_NAME}'."
  echo "You can attach to the session using: tmux attach-session -t ${TMUX_SESSION_NAME}"
  echo "Or list sessions using: tmux ls"
else
  echo "Flask server not started because virtual environment could not be activated."
fi

echo "Redeployment process finished."
