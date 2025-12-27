# Fire Detection App - WebSocket URL Routing
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Main fire detection WebSocket
    re_path(r'ws/fire-detection/$', consumers.FireDetectionConsumer.as_asgi()),
    
    # Camera feed WebSocket for individual cameras
    re_path(r'ws/camera-feed/(?P<camera_id>\w+)/$', consumers.CameraFeedConsumer.as_asgi()),
    
    # Dashboard real-time updates WebSocket
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
]

# WebSocket endpoint documentation:
#
# 1. Fire Detection WebSocket: ws://localhost:8000/ws/fire-detection/
#    - Real-time fire detection updates
#    - Emergency alerts
#    - System status updates
#    - Incident notifications
#
# 2. Camera Feed WebSocket: ws://localhost:8000/ws/camera-feed/{camera_id}/
#    - Live camera feed streaming
#    - Real-time frame processing
#    - Camera-specific alerts
#
# 3. Dashboard WebSocket: ws://localhost:8000/ws/dashboard/
#    - Dashboard real-time data updates
#    - System statistics
#    - Analytics data
#    - Performance metrics
