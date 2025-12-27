@echo off
echo 🔥 FIRE DETECTION SYSTEM - VIDEO CONFIGURATOR
echo ================================================

cd /d "c:\Users\padir\OneDrive\Desktop\fire project\Fire_Detection\Fire_Detection\videos"

echo Current directory: %CD%
echo.

echo Checking if Python is available...
python --version
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo Please ensure Python is installed and added to PATH
    goto end
)

echo.
echo 🚀 Running video configuration script...
echo.

python run_video_config.py

:end
echo.
echo Press any key to continue...
pause > nul
