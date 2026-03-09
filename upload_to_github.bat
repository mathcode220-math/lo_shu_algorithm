@echo off
echo ============================================================
echo Lo Shu Algorithm - GitHub Upload Script
echo ============================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Initialize git repository
echo [Step 1/5] Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo [ERROR] Failed to initialize Git
    pause
    exit /b 1
)
echo [OK] Git initialized
echo.

REM Add all files
echo [Step 2/5] Adding all files...
git add .
echo [OK] Files added
echo.

REM Create commit
echo [Step 3/5] Creating initial commit...
git commit -m "Initial commit: Lo Shu Balance Algorithm v1.0.0"
if %errorlevel% neq 0 (
    echo [WARNING] Commit may have failed (no changes to commit?)
)
echo [OK] Commit created
echo.

REM Get GitHub username from user
echo ============================================================
echo GitHub Information
echo ============================================================
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
if "%GITHUB_USERNAME%"=="" (
    echo [ERROR] Username cannot be empty
    pause
    exit /b 1
)

echo.
echo [Step 4/5] Setting up remote repository...
git remote add origin https://github.com/%GITHUB_USERNAME%/lo_shu_algorithm.git
if %errorlevel% neq 0 (
    echo [WARNING] Remote may already exist
)
echo [OK] Remote configured for: %GITHUB_USERNAME%
echo.

REM Rename branch
echo [Step 5/5] Renaming branch to main...
git branch -M main
echo [OK] Branch renamed
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo.
echo 1. Create repository on GitHub:
echo    https://github.com/new
echo    - Repository name: lo_shu_algorithm
echo    - Description: A novel image denoising algorithm based on Lo Shu Magic Square
echo    - License: GNU AGPL v3.0
echo    - DO NOT add README (we already have one)
echo.
echo 2. Push code to GitHub:
echo    git push -u origin main
echo.
echo 3. Your repository URL will be:
echo    https://github.com/%GITHUB_USERNAME%/lo_shu_algorithm
echo.
echo ============================================================
pause
