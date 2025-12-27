# Fire Detection System - Frontend

This folder contains all the frontend files for the Fire Detection System.

## 📁 Folder Structure

```
frontend/
├── index.html              # Main frontend entry point
├── dashboard.html           # Main dashboard (standalone version)
├── css/                     # Stylesheets
│   └── styles.css          # Main CSS file
├── js/                      # JavaScript files
│   ├── script.js           # Main JavaScript
│   ├── dashboard.js        # Dashboard functionality
│   └── config.js           # Configuration settings
├── images/                  # Image assets
│   ├── fire-kitchen.jpg    # Sample fire detection images
│   └── fire-kitchen-annotated.jpg
└── pages/                   # Individual page templates
    ├── analytics.html      # Analytics page
    ├── camera-feeds.html   # Camera feeds page
    ├── dashboard.html      # Dashboard template (Django version)
    ├── emergency-contacts.html # Emergency contacts page
    ├── incident-history.html  # Incident history page
    ├── index.html          # Landing page template
    ├── launch.html         # System launch page
    └── reports.html        # Reports page
```

## 🚀 Features

### Main Dashboard (`dashboard.html`)
- **Live Camera Feeds**: Real-time monitoring from multiple cameras
- **Fire Detection Status**: Visual indicators for fire detection confidence
- **Emergency Controls**: Quick access to emergency response actions
- **System Statistics**: Live stats on cameras, incidents, and response times
- **Real-time Alerts**: Notifications for fire detection events

### Pages
- **Camera Feeds**: Dedicated camera monitoring interface
- **Incident History**: Historical fire detection events
- **Analytics**: System performance charts and statistics
- **Emergency Contacts**: Management of emergency response contacts
- **Reports**: Generate and view system reports

## 🛠 Technologies Used

- **HTML5**: Modern markup structure
- **CSS3**: Custom styling with responsive design
- **JavaScript**: Interactive functionality and real-time updates
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library for UI elements

## 🎨 Design Features

- **Dark Theme**: Professional dark interface suitable for control rooms
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live data updates without page refresh
- **Emergency UI**: High-contrast alerts and emergency controls
- **Professional Layout**: Clean, organized interface for emergency operators

## 🔧 Usage

### Standalone Frontend
1. Open `index.html` in a web browser
2. Navigate to different sections using the menu
3. Access the main dashboard via `dashboard.html`

### With Django Backend
The templates in the `pages/` folder are designed to work with the Django backend:
- They include Django template tags (`{% load static %}`)
- Static file references use Django's static file system
- Integrated with the backend API endpoints

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔒 Security Features

- **Input Validation**: All form inputs are validated
- **XSS Protection**: Proper escaping of user inputs
- **CSRF Protection**: When integrated with Django backend

## 🚨 Emergency Features

- **One-Click Alerts**: Immediate emergency response activation
- **Visual Alerts**: High-contrast warning indicators
- **Audio Alerts**: Sound notifications for critical events
- **Multi-Channel Notifications**: SMS, email, and in-app alerts

## 🔗 Integration

This frontend is designed to work with:
- **Django Backend**: Full integration with REST API
- **WebSocket Connections**: Real-time data updates
- **External APIs**: Fire department and emergency services
- **Camera Systems**: RTSP and IP camera feeds

## 📈 Performance

- **Optimized Loading**: Efficient asset loading
- **Caching**: Browser caching for static assets
- **Lazy Loading**: Images and content loaded on demand
- **Minimal Dependencies**: Core functionality works with minimal external dependencies

## 🎯 Target Users

- **Emergency Operators**: Control room personnel
- **Security Staff**: Building security teams
- **Fire Safety Officers**: Fire prevention specialists
- **System Administrators**: IT and maintenance staff

## 🔄 Updates

The frontend automatically receives updates when:
- New fire detection events occur
- Camera status changes
- System configuration is modified
- Emergency alerts are triggered

---

**Note**: This frontend is part of a complete Fire Detection System. For full functionality, it should be used with the Django backend located in the `../backend/` directory.
