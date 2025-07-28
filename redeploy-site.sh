#!/bin/bash
set -e  # Exit immediately if any command fails

# Navigate to your project folder
cd /root/Shlok_MLH_Portfolio

# Pull latest changes from GitHub main branch
git fetch && git reset origin/main --hard

# Stop existing containers
docker compose -f docker-compose.prod.yml down

# Start containers again, rebuilding if needed
docker compose -f docker-compose.prod.yml up -d --build
