# Fire Detection System - Complete Startup Script
"""
Complete startup script for the Fire Detection System

This script will:
1. Check dependencies
2. Set up the database
3. Start all required services
4. Launch the system

Usage:
    python start_fire_system.py
"""

import os
import sys
import subprocess
import time
import threading
import platform
from pathlib import Path

def print_banner():
    """Print system banner"""
    banner = """
    🔥🚨 FIRE DETECTION & EMERGENCY RESPONSE SYSTEM 🚨🔥
    ================================================================
    
    Integrated Full-Stack Fire Detection System
    - Frontend: HTML5, CSS3, JavaScript with TailwindCSS
    - Backend: Django with REST API and WebSockets
    - AI Detection: YOLOv8 Computer Vision
    - Real-time Alerts: Celery + Redis
    - Admin Interface: Django Admin
    
    ================================================================
    """
    print(banner)

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking system dependencies...")
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {sys.version}")
    
    # Check if virtual environment exists
    venv_path = Path('venv')
    if not venv_path.exists():
        print("❌ Virtual environment not found. Run setup_backend.py first!")
        return False
    print("✅ Virtual environment found")
    
    # Check if manage.py exists
    if not Path('manage.py').exists():
        print("❌ Django manage.py not found. Make sure you're in the backend directory!")
        return False
    print("✅ Django project found")
    
    return True

def get_commands():
    """Get platform-specific commands"""
    if platform.system() == "Windows":
        return {
            'python': 'venv\\Scripts\\python.exe',
            'pip': 'venv\\Scripts\\pip.exe',
            'activate': 'venv\\Scripts\\activate.bat'
        }
    else:
        return {
            'python': 'venv/bin/python',
            'pip': 'venv/bin/pip',
            'activate': 'source venv/bin/activate'
        }

def run_command(command, cwd=None, background=False):
    """Run a command"""
    try:
        if background:
            return subprocess.Popen(command, shell=True, cwd=cwd)
        else:
            result = subprocess.run(command, shell=True, cwd=cwd, 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Command failed: {command}")
                print(f"Error: {result.stderr}")
                return False
            return True
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def setup_database():
    """Set up Django database"""
    print("📊 Setting up database...")
    
    commands = get_commands()
    python_cmd = commands['python']
    
    # Run migrations
    print("  - Making migrations...")
    if not run_command(f"{python_cmd} manage.py makemigrations"):
        return False
    
    print("  - Running migrations...")
    if not run_command(f"{python_cmd} manage.py migrate"):
        return False
    
    # Collect static files
    print("  - Collecting static files...")
    run_command(f"{python_cmd} manage.py collectstatic --noinput")
    
    # Initialize fire detection system
    print("  - Initializing fire detection system...")
    run_command(f"{python_cmd} manage.py init_fire_system")
    
    print("✅ Database setup complete")
    return True

def start_redis():
    """Start Redis server"""
    print("🔴 Starting Redis server...")
    
    # Check if Redis is already running
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis is already running")
        return True
    except:
        pass
    
    # Try to start Redis
    if platform.system() == "Windows":
        # On Windows, Redis might be installed via WSL or as a service
        print("📝 Please start Redis manually:")
        print("   - Install Redis for Windows or use WSL")
        print("   - Run: redis-server")
        input("Press Enter when Redis is running...")
    else:
        # Try to start Redis on Unix systems
        redis_process = run_command("redis-server", background=True)
        time.sleep(2)
        if redis_process:
            print("✅ Redis server started")
            return redis_process
    
    return True

def start_celery():
    """Start Celery worker"""
    print("⚡ Starting Celery worker...")
    
    commands = get_commands()
    python_cmd = commands['python']
    
    celery_cmd = f"{python_cmd} -m celery -A fire_detection_backend worker -l info"
    celery_process = run_command(celery_cmd, background=True)
    
    if celery_process:
        print("✅ Celery worker started")
        return celery_process
    return None

def start_django():
    """Start Django development server"""
    print("🌐 Starting Django development server...")
    
    commands = get_commands()
    python_cmd = commands['python']
    
    django_cmd = f"{python_cmd} manage.py runserver 127.0.0.1:8000"
    django_process = run_command(django_cmd, background=True)
    
    if django_process:
        print("✅ Django server started at http://127.0.0.1:8000")
        return django_process
    return None

def print_access_info():
    """Print access information"""
    info = """
    🎯 SYSTEM ACCESS POINTS:
    ================================================================
    
    🏠 Main Interface:        http://127.0.0.1:8000/
    📊 Dashboard:             http://127.0.0.1:8000/dashboard/
    📹 Camera Feeds:          http://127.0.0.1:8000/camera-feeds/
    📈 Analytics:             http://127.0.0.1:8000/analytics/
    📞 Emergency Contacts:    http://127.0.0.1:8000/emergency-contacts/
    📄 Reports:               http://127.0.0.1:8000/reports/
    🗂️  Incident History:     http://127.0.0.1:8000/incident-history/
    
    🔧 API Endpoints:         http://127.0.0.1:8000/api/
    👤 Admin Interface:       http://127.0.0.1:8000/admin/
    
    ================================================================
    
    🎮 SYSTEM CONTROLS:
    - Press Ctrl+C to stop all services
    - Check logs for any issues
    - Admin login required for backend management
    
    🔧 DEVELOPMENT NOTES:
    - Frontend files: backend/templates/ and backend/static/
    - API documentation: http://127.0.0.1:8000/api/
    - Real-time WebSocket endpoints available
    - Background task processing active
    
    ================================================================
    """
    print(info)

def monitor_processes(processes):
    """Monitor running processes"""
    print("🔍 Monitoring system processes...")
    print("Press Ctrl+C to stop all services")
    
    try:
        while True:
            time.sleep(5)
            # Check if processes are still running
            for name, process in processes.items():
                if process and hasattr(process, 'poll'):
                    if process.poll() is not None:
                        print(f"⚠️  {name} process stopped unexpectedly")
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        
        # Stop all processes
        for name, process in processes.items():
            if process and hasattr(process, 'terminate'):
                try:
                    process.terminate()
                    print(f"✅ Stopped {name}")
                except:
                    pass
        
        print("🔥 Fire Detection System stopped successfully!")

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed!")
        sys.exit(1)
    
    processes = {}
    
    try:
        # Start Redis
        redis_process = start_redis()
        if redis_process and hasattr(redis_process, 'poll'):
            processes['Redis'] = redis_process
        
        # Start Celery
        celery_process = start_celery()
        if celery_process:
            processes['Celery'] = celery_process
        
        # Give services time to start
        print("⏳ Waiting for services to initialize...")
        time.sleep(3)
        
        # Start Django
        django_process = start_django()
        if django_process:
            processes['Django'] = django_process
        
        # Wait for Django to start
        time.sleep(3)
        
        # Print access information
        print_access_info()
        
        # Monitor processes
        monitor_processes(processes)
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        
        # Clean up processes
        for name, process in processes.items():
            if process and hasattr(process, 'terminate'):
                try:
                    process.terminate()
                except:
                    pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
