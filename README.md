# 🔥 AI-Powered Fire Detection System

An intelligent fire detection and monitoring system using YOLOv8 AI model with automatic email alerts and real-time camera feed monitoring.

## 🌟 Features

- **AI-Powered Detection**: YOLOv8 model for accurate fire and smoke detection
- **Real-Time Monitoring**: Live camera feed monitoring with instant alerts
- **Automatic Email Alerts**: Sends emergency emails to all registered contacts when fire is detected
- **Progressive Detection**: Multi-stage fire detection (Smoke Alert → Fire Development → Fire Accident)
- **Dashboard**: Modern web interface with real-time statistics and camera status
- **Incident History**: Complete log of all fire detection events
- **Emergency Contacts Management**: Easy management of emergency contact list
- **Video Upload**: Support for analyzing uploaded video footage
- **Reports Generation**: Automated fire incident reports

## 🚀 Tech Stack

- **Backend**: Django 4.2.5, Python 3.8+
- **AI/ML**: YOLOv8 (Ultralytics), OpenCV
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Email**: Gmail SMTP with automatic alerts
- **Database**: SQLite (Django ORM)
- **Task Queue**: Celery + Redis (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Gmail account with App Password (for email alerts)

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fire-detection-system.git
cd fire-detection-system
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
cd "fire project - Copy\Fire_Detection\Fire_Detection\backend"
pip install -r requirements.txt
```

4. **Configure email settings**
Edit `backend/fire_detection_backend/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Create superuser (admin)**
```bash
python manage.py createsuperuser
```

7. **Add emergency contacts**
```bash
python setup_emergency_contacts.py
```

## 🎯 Usage

### Starting the System

**Option 1: Using Batch File (Windows)**
```bash
cd "fire project - Copy\Fire_Detection\Fire_Detection\backend"
START.bat
```

**Option 2: Manual Start**
```bash
cd "fire project - Copy\Fire_Detection\Fire_Detection\backend"
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

### Main Pages

- **Dashboard**: `http://127.0.0.1:8000/dashboard/`
- **Camera Feeds**: `http://127.0.0.1:8000/camera-feeds/`
- **Emergency Contacts**: `http://127.0.0.1:8000/emergency-contacts/`
- **Incident History**: `http://127.0.0.1:8000/incident-history/`
- **Reports**: `http://127.0.0.1:8000/reports/`

## 📧 Email Alert System

The system automatically sends emergency emails when fire is detected:

1. **Fire Detected** → System triggers alert
2. **Modal Popup** → Shows fire details with sound alarm
3. **Automatic Emails** → Sent to all registered emergency contacts
4. **Email Content**: 
   - Camera name and location
   - Fire confidence level
   - Timestamp
   - People count in area
   - Emergency response recommendations

### Email Configuration

1. Enable 2-Factor Authentication in your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security
   - 2-Step Verification → App Passwords
   - Generate password for "Mail"
3. Use this App Password in settings.py

## 🎥 Video Configuration

Upload test videos for fire detection:
```bash
cd "fire project - Copy\Fire_Detection\Fire_Detection\videos"
python upload_mall_video.py
```

## 🔐 Security Notes

- Never commit sensitive data (passwords, API keys) to GitHub
- Use environment variables for sensitive configuration
- Keep `.env` files in `.gitignore`
- Use Django's `SECRET_KEY` properly in production

## 📊 System Architecture

```
Frontend (HTML/JS/CSS)
    ↓
Django REST API
    ↓
YOLOv8 AI Model → Fire Detection
    ↓
Email Service → SMTP Gmail
    ↓
Emergency Contacts → Notifications
```

## 🛠️ Testing

Test the email alert system:
```bash
python test_fire_email_alerts.py
```

## 📱 API Endpoints

- `POST /api/fire-detection/trigger_manual_fire_alert/` - Trigger manual fire alert
- `GET /api/confidence-live/` - Get live confidence data
- `GET /api/fire-detection/stats/` - Get fire detection statistics
- `GET /api/emergency-contacts/` - List emergency contacts

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Rishi** - Initial work

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- Django Framework
- OpenCV Community
- TailwindCSS

## 📞 Support

For support, email padirishitha13@gmail.com

## 🚨 Emergency Response

When fire is detected:
1. ✅ System sends automatic emails to all contacts
2. ✅ Fire alarm sound plays on dashboard
3. ✅ Red alert modal displays fire details
4. ✅ Incident logged in database
5. ✅ Real-time updates on all connected devices

---

**⚠️ Important**: This system is designed to assist fire detection but should not replace professional fire safety equipment and procedures.
