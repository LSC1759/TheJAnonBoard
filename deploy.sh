#!/bin/bash
set -e  # Exit immediately if a command fails

# Navigate to repo
cd /var/www/TheJAnonBoard || exit

# Fetch latest changes
git fetch origin

# Get current commit hashes
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date) - Updates detected. Deploying..."
    
    # Reset local branch to match remote
    git reset --hard origin/main

    # Activate virtualenv
    source venv/bin/activate

    # Install/update dependencies
    pip install --upgrade pip
    pip install -r requirements.txt

    # Deactivate venv
    deactivate

    # Restart Gunicorn
    sudo systemctl restart TheJAnonBoard

    # Log success
    echo "$(date) - Deployment completed successfully" >> deploy.log
else
    echo "$(date) - No updates found. Gunicorn not restarted." >> deploy.log
fi
