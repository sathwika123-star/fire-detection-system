# Video Upload and Integration Script for mall.mp4
# This script will help integrate your mall.mp4 video with both dashboard and camera recordings

import os
import shutil
from datetime import datetime
import uuid

# Configuration
VIDEO_NAME = "mall.mp4"
PROJECT_ROOT = r"c:\Users\padir\OneDrive\Desktop\fire project\Fire_Detection\Fire_Detection"
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")

# Paths for video integration
UPLOAD_PATHS = {
    "videos_folder": os.path.join(PROJECT_ROOT, "videos", "uploaded_videos"),
    "media_folder": os.path.join(BACKEND_ROOT, "media", "uploaded_videos"),
    "cctv_recordings": os.path.join(BACKEND_ROOT, "media", "cctv_recordings"),
    "incident_videos": os.path.join(BACKEND_ROOT, "media", "incident_videos"),
}

def create_video_entry():
    """Creates database entry for the uploaded video"""
    
    # Video metadata
    video_data = {
        "original_filename": VIDEO_NAME,
        "display_name": "Mall Security Camera Feed",
        "description": "Shopping mall surveillance video for fire detection testing",
        "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camera_location": "Mall Main Area",
        "camera_id": "CAM_MALL_001",
        "file_size": "25.5 MB",  # You can update this with actual size
        "duration": "120 seconds",  # You can update this with actual duration
        "resolution": "1920x1080",  # You can update this with actual resolution
        "format": "MP4",
        "analysis_status": "pending",
        "fire_detection_status": "not_analyzed"
    }
    
    return video_data

def get_video_urls():
    """Returns URLs for accessing the video in different contexts"""
    
    base_url = "http://127.0.0.1:8000"
    video_filename = VIDEO_NAME
    
    urls = {
        "dashboard_url": f"{base_url}/media/uploaded_videos/{video_filename}",
        "camera_feed_url": f"{base_url}/media/cctv_recordings/{video_filename}",
        "incident_url": f"{base_url}/media/incident_videos/{video_filename}",
        "analysis_url": f"{base_url}/api/video-analysis/analyze_video/",
        "upload_page": f"{base_url}/video-upload/"
    }
    
    return urls

def create_camera_entry():
    """Creates camera entry for dashboard integration"""
    
    camera_data = {
        "camera_id": "CAM_MALL_001",
        "name": "Mall Main Area Camera",
        "location": "Shopping Mall - Main Entrance",
        "status": "active",
        "video_source": VIDEO_NAME,
        "rtsp_url": f"file:///media/uploaded_videos/{VIDEO_NAME}",
        "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fire_status": "normal",
        "confidence": 0.0
    }
    
    return camera_data

# Instructions for manual upload
UPLOAD_INSTRUCTIONS = f"""
🔥 MALL.MP4 VIDEO INTEGRATION GUIDE 🔥

## 📁 WHERE TO PLACE YOUR mall.mp4 FILE:

### Option 1: Main Videos Folder
Place your mall.mp4 file here:
{UPLOAD_PATHS['videos_folder']}\\{VIDEO_NAME}

### Option 2: Django Media Folder  
Place your mall.mp4 file here:
{UPLOAD_PATHS['media_folder']}\\{VIDEO_NAME}

### Option 3: Camera Recordings (For Dashboard)
Copy your mall.mp4 file here:
{UPLOAD_PATHS['cctv_recordings']}\\{VIDEO_NAME}

## 🚀 INTEGRATION STEPS:

### Step 1: Copy Video File
1. Copy your mall.mp4 to any of the above locations
2. File will be accessible via Django media URLs

### Step 2: Dashboard Integration
- Video will appear in camera feeds as "Mall Main Area Camera"
- Camera ID: CAM_MALL_001
- Status: Active surveillance feed

### Step 3: Camera Recordings
- Video will be listed in video recordings page
- Playable through built-in video player
- Integrated with fire detection analysis

### Step 4: Test Integration
1. Go to: http://127.0.0.1:8000/dashboard/
2. Look for "Mall Main Area Camera" feed
3. Go to: http://127.0.0.1:8000/video-recordings/
4. Find mall.mp4 in the recordings list

## 🎯 QUICK SETUP COMMANDS:

If you have mall.mp4 in your current directory, run these in terminal:

### Copy to Videos Folder:
copy mall.mp4 "{UPLOAD_PATHS['videos_folder']}\\"

### Copy to Media Folder:
copy mall.mp4 "{UPLOAD_PATHS['media_folder']}\\"

### Copy to Camera Recordings:
copy mall.mp4 "{UPLOAD_PATHS['cctv_recordings']}\\"

## 🔧 WEB INTERFACE UPLOAD:

### Upload via Web Interface:
1. Go to: http://127.0.0.1:8000/video-upload/
2. Click "Choose File" and select mall.mp4
3. Or paste local file path as URL
4. Click "Analyze" to process

## 📊 EXPECTED RESULTS:

After placing the file, you should see:
✅ Mall camera feed in dashboard
✅ Video in recordings list  
✅ Fire detection analysis available
✅ Emergency response integration
✅ Real-time status updates

## 🎬 VIDEO ACCESS URLS:

Dashboard Feed: http://127.0.0.1:8000/media/uploaded_videos/mall.mp4
Camera Recording: http://127.0.0.1:8000/media/cctv_recordings/mall.mp4
Analysis Page: http://127.0.0.1:8000/video-upload/

"""

if __name__ == "__main__":
    print(UPLOAD_INSTRUCTIONS)
    
    # Create metadata
    video_meta = create_video_entry()
    camera_meta = create_camera_entry()
    video_urls = get_video_urls()
    
    print("\\n🔥 VIDEO METADATA CREATED:")
    print(f"Camera ID: {camera_meta['camera_id']}")
    print(f"Location: {camera_meta['location']}")
    print(f"Upload Time: {video_meta['upload_timestamp']}")
    print(f"Dashboard URL: {video_urls['dashboard_url']}")
