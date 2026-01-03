@echo off
echo ====================================
echo    Fire Detection System Server
echo ====================================
echo.
echo Starting Django Development Server...
echo.

cd "C:\Users\padir\OneDrive\Desktop\Fire_Detection\Fire_Detection\backend"

echo Current directory: %CD%
echo.
echo Starting server on http://127.0.0.1:8000/
echo.
echo ====================================
echo    Server is now running!
echo    Access at: http://127.0.0.1:8000/
echo    Press Ctrl+C to stop the server
echo ====================================
echo.

python manage.py runserver

pause
