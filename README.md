# 🔥 Fire Detection System

## Simple AI-Powered Fire Detection with Django

### Quick Start

1. **Start the server:**
   ```
   Double-click START.bat
   ```

2. **Open your browser:**
   ```
   http://127.0.0.1:8000
   ```

### Features

- ✅ Real-time fire detection using AI (YOLOv8)
- ✅ Camera feed monitoring
- ✅ Email alerts to emergency contacts
- ✅ Incident history and reports
- ✅ Analytics dashboard
- ✅ Video analysis

### Project Structure

```
Fire_Detection/
├── START.bat              # Quick start script
├── requirements.txt       # Python dependencies
└── backend/
    ├── manage.py         # Django management
    ├── fire_detection/   # Main app
    ├── templates/        # HTML pages
    ├── static/          # CSS, JS, images
    └── media/           # Uploaded files
```

### Configuration

Edit `backend/.env` to configure:
- Email settings (Gmail SMTP)
- Emergency contacts
- Detection sensitivity

### Support

For issues, check the Django server logs in the terminal.
