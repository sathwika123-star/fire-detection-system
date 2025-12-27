#!/usr/bin/env python3
"""
Simple Video Configuration Runner
This script will configure your fire detection videos properly.
"""

import os
import shutil
from pathlib import Path

def main():
    try:
        print("🔥 FIRE DETECTION VIDEO CONFIGURATOR")
        print("=" * 50)
        
        # Get current directory
        current_dir = Path(__file__).parent
        print(f"Working directory: {current_dir}")
        
        # Define paths
        fire_dir = current_dir / "fire_incidents"
        normal_dir = current_dir / "normal_videos"
        media_dir = current_dir.parent / "backend" / "media" / "uploaded_videos"
        
        print(f"\nChecking directories:")
        print(f"Fire incidents: {fire_dir}")
        print(f"Normal videos: {normal_dir}")
        print(f"Media target: {media_dir}")
        
        # Create media directory if needed
        media_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Media directory ready")
        
        # List and copy fire incident videos
        copied_files = []
        
        if fire_dir.exists():
            print(f"\n🔥 FIRE INCIDENT VIDEOS:")
            for video_file in fire_dir.glob("*.mp4"):
                print(f"  Found: {video_file.name}")
                # Copy to media with safe filename
                safe_name = video_file.name.replace(" ", "_")
                dest_path = media_dir / safe_name
                shutil.copy2(video_file, dest_path)
                print(f"  ✅ Copied to: {safe_name}")
                copied_files.append(safe_name)
        else:
            print(f"❌ Fire incidents directory not found")
        
        if normal_dir.exists():
            print(f"\n✅ NORMAL VIDEOS:")
            for video_file in normal_dir.glob("*.mp4"):
                print(f"  Found: {video_file.name}")
                # Copy to media with safe filename
                safe_name = video_file.name.replace(" ", "_")
                dest_path = media_dir / safe_name
                shutil.copy2(video_file, dest_path)
                print(f"  ✅ Copied to: {safe_name}")
                copied_files.append(safe_name)
        else:
            print(f"❌ Normal videos directory not found")
        
        print(f"\n📊 SUMMARY:")
        print(f"Total files copied: {len(copied_files)}")
        for file in copied_files:
            print(f"  • {file}")
        
        print(f"\n🎉 VIDEO CONFIGURATION COMPLETE!")
        print(f"Your videos are now ready for the fire detection system.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
    input("\nPress Enter to continue...")
