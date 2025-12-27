# Fire Detection App - Django App Module
"""
Fire Detection Django Application

This module provides a comprehensive fire detection system with the following features:

Core Components:
- Real-time fire detection using AI/ML models (YOLOv8)
- Camera management and monitoring
- Emergency alert system
- Incident tracking and reporting
- System configuration management

Key Features:
- Multi-camera support with live feed processing
- Automatic fire detection with configurable sensitivity
- Emergency contact management with priority levels
- Real-time WebSocket notifications
- Background task processing for alerts
- Administrative interface for system management
- RESTful API for frontend integration

Models:
- Camera: Manages IP cameras and their configurations
- FireDetectionEvent: Tracks fire detection incidents
- EmergencyContact: Manages emergency response contacts
- SystemConfiguration: System-wide settings and preferences

API Endpoints:
- /api/cameras/ - Camera management
- /api/fire-detection/ - Fire detection events
- /api/emergency-contacts/ - Emergency contacts
- /api/system-config/ - System configuration

WebSocket Endpoints:
- /ws/fire-detection/ - Real-time fire alerts
- /ws/camera-feed/{id}/ - Live camera feeds
- /ws/dashboard/ - Dashboard updates

Background Tasks:
- Fire detection processing
- Emergency notifications (SMS, Email)
- System health monitoring
- Data cleanup and maintenance

Usage:
    This app integrates with a Django project to provide fire detection
    capabilities. It requires Redis for caching and Celery for background tasks.
    
    Example configuration in settings.py:
    
    INSTALLED_APPS = [
        ...
        'fire_detection',
        'rest_framework',
        'corsheaders',
        'channels',
    ]
    
    # Add to your project's urls.py:
    urlpatterns = [
        path('', include('fire_detection.urls')),
    ]

Dependencies:
- Django 4.2+
- Django REST Framework
- Django Channels (WebSockets)
- Celery (Background tasks)
- Redis (Caching/Message broker)
- OpenCV (Computer vision)
- YOLOv8/Ultralytics (AI detection)
- Pillow (Image processing)

Author: Fire Detection System Team
Version: 1.0.0
"""

# Version information
__version__ = '1.0.0'
__author__ = 'Fire Detection System Team'

# Default app configuration
default_app_config = 'fire_detection.apps.FireDetectionConfig'
