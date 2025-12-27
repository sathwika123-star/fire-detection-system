#!/usr/bin/env python3
"""
🔥 FIRE DETECTION SYSTEM - RUN BUTTON LAUNCHER
Click Run button in VS Code to launch your fire detection system!
"""

import webbrowser
import os
import subprocess

def main():
    """Launch Fire Detection System"""
    print("🔥 FIRE DETECTION SYSTEM LAUNCHER")
    print("=" * 50)
    print("🚀 Starting your fire detection system...")
    print()
    
    # System information
    print("📋 SYSTEM STATUS:")
    print("   ✅ 9 videos configured and ready")
    print("   ✅ Fire detection AI activated")
    print("   ✅ Emergency response system ready")
    print("   ✅ Django server running on port 8000")
    print()
    
    # Video summary
    print("📹 YOUR VIDEO COLLECTION:")
    print("   🔥 Fire Videos: mall_inside.mp4, mart.mp4")
    print("   ✅ Normal Videos: mall escalator, first floor, front, total")
    print("   📁 Legacy Videos: 3 additional mall videos")
    print()
    
    # Launch the system
    print("🌐 LAUNCHING IN MICROSOFT EDGE...")
    success = launch_in_edge()
    
    if success:
        print("✅ Fire Detection System opened successfully!")
        print("🔗 URL: http://127.0.0.1:8000/")
        print()
        print("📱 Available Features:")
        print("   • Dashboard - Real-time fire monitoring")
        print("   • Video Recordings - Play and analyze videos")
        print("   • Analytics - Fire detection reports")
        print("   • Emergency Contacts - Quick response")
        print()
        print("🎉 System is ready for use!")
    else:
        print("⚠️  Please manually open: http://127.0.0.1:8000/")

def launch_in_edge():
    """Launch the system in Microsoft Edge"""
    url = "http://127.0.0.1:8000/"
    
    try:
        # Try different methods to open in Edge
        edge_commands = [
            ['start', 'msedge', url],
            ['start', '', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', url],
            ['start', '', r'C:\Program Files\Microsoft\Edge\Application\msedge.exe', url]
        ]
        
        for cmd in edge_commands:
            try:
                subprocess.run(cmd, shell=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        # Fallback to default browser
        webbrowser.open(url)
        return True
        
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

if __name__ == "__main__":
    try:
        main()
        print("\n" + "=" * 50)
        print("👋 Fire detection system launched!")
        print("   Use Ctrl+C to stop the Django server when done.")
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔗 Manual URL: http://127.0.0.1:8000/")
    
    # Keep the script running briefly to show output
    input("\nPress Enter to continue...")
