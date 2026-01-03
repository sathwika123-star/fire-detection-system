@echo off
echo ========================================
echo Installing Real AI Fire Detection Dependencies
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call backend\fire_detection_env\Scripts\activate

echo [2/4] Installing PyTorch (CPU version for compatibility)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo [3/4] Installing YOLOv8 and AI dependencies...
pip install -r backend\requirements_ai.txt

echo [4/4] Installing additional dependencies...
pip install Pillow>=8.0.0
pip install numpy>=1.21.0
pip install opencv-python>=4.5.0

echo.
echo ========================================
echo Real AI Fire Detection Setup Complete!
echo ========================================
echo.
echo 🤖 AI Dependencies Installed:
echo   ✅ PyTorch (CPU version)
echo   ✅ YOLOv8 (Ultralytics)
echo   ✅ OpenCV
echo   ✅ Additional ML libraries
echo.
echo 🚀 Next steps:
echo   1. Start the backend server: cd backend && python manage.py runserver 127.0.0.1:8001
echo   2. Open dashboard: http://127.0.0.1:8001/dashboard/
echo   3. Real AI detection will activate automatically
echo.
echo ⚠️  Note: First run may take longer as YOLOv8 downloads the model weights
echo.
pause
