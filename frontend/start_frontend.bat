@echo off
echo Starting Fire Detection System Frontend...
echo.

REM Check if a local web server is available
where python >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Python HTTP Server...
    echo Frontend will be available at: http://localhost:8080
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    cd /d "%~dp0"
    python -m http.server 8080
) else (
    echo Python not found. Opening frontend files directly...
    echo.
    start "" "index.html"
)

pause
