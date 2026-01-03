@echo off
echo ====================================
echo  Real AI Fire Detection System Server
echo ====================================
echo.
echo Starting Django Development Server with AI Detection...
echo.

cd "C:\Users\padir\OneDrive\Desktop\fire project\Fire_Detection\Fire_Detection\backend"

echo Current directory: %CD%
echo.
echo Installing/Checking AI Dependencies...
pip install ultralytics torch opencv-python numpy
echo.
echo Starting server on http://127.0.0.1:8001/
echo.
echo ====================================
echo    Real AI Fire Detection Server Running!
echo    Access Dashboard: http://127.0.0.1:8001/dashboard/
echo    Access Camera Feeds: http://127.0.0.1:8001/camera-feeds/
echo    Press Ctrl+C to stop the server
echo ====================================
echo.

python manage.py runserver 127.0.0.1:8001

pause
