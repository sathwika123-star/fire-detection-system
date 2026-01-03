#!/usr/bin/env python
"""
Direct Django Server Launcher for Real AI Fire Detection System
This script directly starts the Django server from the correct location
"""

import os
import sys
import subprocess
from pathlib import Path

def start_server():
    """Start the Django server directly"""
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Navigate to the backend directory
    backend_dir = script_dir / "Fire_Detection" / "backend"
    
    print(f"🚀 Starting Real AI Fire Detection System")
    print(f"📁 Backend directory: {backend_dir}")
    
    if not backend_dir.exists():
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    # Check if manage.py exists
    manage_py = backend_dir / "manage.py"
    if not manage_py.exists():
        print(f"❌ manage.py not found: {manage_py}")
        return False
    
    # Change to backend directory
    os.chdir(str(backend_dir))
    print(f"📂 Changed to directory: {os.getcwd()}")
    
    # Run Django server
    print("🤖 Starting Django server with Real AI Fire Detection...")
    print("🌐 Server will be available at: http://127.0.0.1:8001/")
    print("📊 Dashboard: http://127.0.0.1:8001/dashboard/")
    print("📹 Camera Feeds: http://127.0.0.1:8001/camera-feeds/")
    print()
    print("⚠️  First run may take longer as AI models are loaded...")
    print("🤖 Real AI Detection will activate automatically!")
    print()
    
    try:
        # Start the Django development server
        result = subprocess.run([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8001"
        ], check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔥 Real AI Fire Detection System Launcher")
    print("=" * 50)
    
    success = start_server()
    
    if success:
        print("\n✅ Server started successfully!")
    else:
        print("\n❌ Failed to start server")
        print("\n💡 Manual steps:")
        print("1. Open terminal/command prompt")
        print("2. Navigate to: Fire_Detection/Fire_Detection/backend/")
        print("3. Run: python manage.py runserver 127.0.0.1:8001")
    
    input("\nPress Enter to continue...")
