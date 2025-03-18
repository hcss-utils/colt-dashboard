@echo off
echo Setting Heroku API key...
set HEROKU_API_KEY=39b55975-1720-4ef9-b874-3ea8ea43f6fb

echo Checking if Heroku CLI is installed...
where heroku >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Heroku CLI not found. Please install it first.
    echo Visit: https://devcenter.heroku.com/articles/heroku-cli
    exit /b 1
)

set APP_NAME=colt-dashboard

echo Checking if app exists...
heroku apps:info -a %APP_NAME% >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Creating Heroku app: %APP_NAME%
    heroku create %APP_NAME%
) else (
    echo Heroku app %APP_NAME% already exists
)

echo Checking if Git is initialized...
if not exist .git (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit"
)

echo Checking if Heroku remote is set...
git remote | findstr "heroku" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Adding Heroku remote...
    heroku git:remote -a %APP_NAME%
)

echo Deploying to Heroku...
git push heroku master

echo Opening app in browser...
heroku open

echo Deployment complete!