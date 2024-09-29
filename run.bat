@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

echo Python is installed, proceeding...

:: Install the required packages
python -m pip install -r requirements.txt

:: Apply database migrations
python manage.py migrate

:: Start the Django development server
python manage.py runserver 0.0.0.0:8000
