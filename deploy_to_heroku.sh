#!/bin/bash

# Set your Heroku API key
export HEROKU_API_KEY=39b55975-1720-4ef9-b874-3ea8ea43f6fb

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI not found. Please install it first."
    echo "Run: curl https://cli-assets.heroku.com/install.sh | sh"
    exit 1
fi

# Set app name
APP_NAME=colt-dashboard

# Check if app exists
if ! heroku apps:info -a $APP_NAME &> /dev/null; then
    echo "Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    echo "Heroku app $APP_NAME already exists"
fi

# Check if Git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if Heroku remote is set
if ! git remote | grep heroku &> /dev/null; then
    echo "Adding Heroku remote..."
    heroku git:remote -a $APP_NAME
fi

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku master

# Open the app in browser
echo "Opening app in browser..."
heroku open

echo "Deployment complete!"
