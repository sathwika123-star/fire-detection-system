@echo off
title Fire Detection System Launcher
color 0A

echo.
echo ========================================
echo 🔥 FIRE DETECTION SYSTEM LAUNCHER 🔥
echo ========================================
echo.

echo 🚀 Starting Django Server...
cd /d "c:\Users\padir\OneDrive\Desktop\fire project\Fire_Detection\Fire_Detection\backend"

echo 📋 Checking if server is already running...
netstat -an | find "8000" > nul
if %errorlevel% == 0 (
    echo ✅ Server already running on port 8000
    goto open_browser
)

echo 🔧 Starting Django development server...
start "Django Server" cmd /k "python manage.py runserver"

echo ⏳ Waiting for server to start...
timeout /t 5 /nobreak > nul

:open_browser
echo.
echo 🌐 Opening Fire Detection System in Microsoft Edge...

:: Try to open in Edge
set "edge_path=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if exist "%edge_path%" (
    echo ✅ Found Microsoft Edge, opening system...
    start "" "%edge_path%" "http://127.0.0.1:8000/"
    goto success
)

set "edge_path=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
if exist "%edge_path%" (
    echo ✅ Found Microsoft Edge, opening system...
    start "" "%edge_path%" "http://127.0.0.1:8000/"
    goto success
)

:: Fallback to default browser
echo ⚠️  Microsoft Edge not found, opening in default browser...
start "" "http://127.0.0.1:8000/"

:success
echo.
echo 🎉 Fire Detection System is now running!
echo 🔗 URL: http://127.0.0.1:8000/
echo.
echo Features available:
echo   📱 Dashboard - Real-time fire monitoring
echo   📹 Video Recordings - View and analyze videos
echo   📊 Analytics - Fire detection reports
echo   📞 Emergency Contacts - Quick emergency response
echo.
echo Press any key to continue...
pause > nul
