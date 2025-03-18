@echo off
echo Setting up GitHub repository...

set REPO_NAME=colt-dashboard

echo Checking if GitHub CLI is installed...
where gh >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo GitHub CLI not found. Please install it first.
    echo Visit: https://cli.github.com/
    exit /b 1
)

echo Checking GitHub authentication...
gh auth status >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Please authenticate with GitHub first using 'gh auth login'
    exit /b 1
)

echo Creating GitHub repository: %REPO_NAME%
gh repo create %REPO_NAME% --private --confirm

echo Adding GitHub remote...
for /f %%i in ('gh api user ^| jq -r .login') do set GH_USERNAME=%%i
git remote add origin https://github.com/%GH_USERNAME%/%REPO_NAME%.git

echo Pushing to GitHub...
git push -u origin master

echo Code successfully pushed to GitHub!