@echo off
title Real AI Fire Detection Server
cls

echo ========================================
echo   🤖 Real AI Fire Detection System
echo ========================================
echo.
echo Starting server with AI capabilities...
echo.

REM Navigate to the correct backend directory
cd /d "C:\Users\padir\OneDrive\Desktop\fire project\Fire_Detection\Fire_Detection\backend"

echo Current directory: %CD%
echo.

REM Check if we're in the right place
if not exist "manage.py" (
    echo ❌ Error: manage.py not found!
    echo Please check the directory structure.
    pause
    exit /b 1
)

echo ✅ Found manage.py - starting Django server...
echo.
echo 🌐 Server URL: http://127.0.0.1:8001/
echo 📊 Dashboard: http://127.0.0.1:8001/dashboard/
echo 📹 Camera Feeds: http://127.0.0.1:8001/camera-feeds/
echo.
echo 🤖 Real AI Detection will activate automatically!
echo ⚠️  First run may take longer as AI models load...
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Django server
python manage.py runserver 127.0.0.1:8001

echo.
echo Server stopped.
pause
