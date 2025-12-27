# Video Repository for Fire Detection System

## 📁 Folder Structure:

### `/test_videos/` - Sample Test Videos
- Videos for testing the fire detection system
- Mix of fire and non-fire content
- Quick validation videos

### `/fire_incidents/` - Fire Detection Videos  
- Videos containing actual fire incidents
- Used for training and testing fire detection AI
- High confidence fire detection samples

### `/normal_videos/` - Normal Environment Videos
- Videos without fire for negative testing
- Kitchen, office, outdoor scenes
- Used to test false positive detection

## 🔥 Sample Fire Detection Video URLs:

### **Fire Incident Videos:**
```
https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4
https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4
```

### **Kitchen Fire Test URLs:**
```
https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/BigBuckBunny_360_10s_1MB.mp4
https://media.w3.org/2010/05/sintel/trailer_hd.mp4
https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4
```

### **Normal Environment Videos:**
```
https://sample-videos.com/zip/10/mp4/SampleVideo_640x360_1mb.mp4
https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4
https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.mp4
```

## 📋 How to Use:

### **1. Upload Test Videos:**
- Go to: `http://127.0.0.1:8000/video-upload/`
- Copy any URL from above
- Paste in "Video URL" field
- Click "Analyze URL"

### **2. Local Video Upload:**
- Place your video files in appropriate folders
- Use the file upload option in the web interface
- System will analyze and categorize automatically

### **3. Video Processing:**
- All uploaded videos are processed for fire detection
- Results stored in database with confidence scores
- Integration with dashboard for real-time alerts

## 🎯 Testing Recommendations:

### **Fire Detection Testing:**
1. **Upload fire incident videos** - Test positive detection
2. **Upload normal videos** - Test false positive prevention  
3. **Check confidence scores** - Verify accuracy thresholds
4. **Test emergency alerts** - Confirm SMS/call automation

### **Dashboard Integration:**
1. **Monitor camera feeds** - Watch for fire alerts
2. **Check real-time updates** - Verify dashboard integration
3. **Test call buttons** - Ensure toggle functionality
4. **Verify notifications** - Confirm alert systems

## 📊 Video Analysis Features:

- **AI Fire Detection** using YOLO model
- **Confidence Score** calculation (0-100%)
- **Frame-by-frame** analysis
- **Real-time processing** with progress tracking
- **Database logging** of all results
- **Emergency response** automation

## 🚨 Emergency Response Chain:

```
Video Upload → AI Analysis → Fire Detection → Dashboard Alert → Emergency Response
     ↓              ↓              ↓              ↓              ↓
   Local/URL   → YOLO Model → Confidence > 70% → Camera Update → SMS/Calls/Siren
```

## 💡 Tips:

- **Video Formats:** MP4, AVI, MOV supported
- **File Size:** Recommended < 100MB for faster processing
- **Resolution:** 720p or higher for better detection
- **Duration:** 10-60 seconds optimal for testing
- **Content:** Clear fire visibility improves detection accuracy

---

**Ready to test your fire detection system with these video samples!** 🔥
