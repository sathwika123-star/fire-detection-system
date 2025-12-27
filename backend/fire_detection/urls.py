# Fire Detection App URLs
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'fire-detection', views.FireDetectionViewSet, basename='fire-detection')
router.register(r'cameras', views.CameraViewSet, basename='cameras')
router.register(r'emergency-contacts', views.EmergencyContactViewSet, basename='emergency-contacts')
router.register(r'system-config', views.SystemConfigurationViewSet, basename='system-config')
# Temporarily commented out - VideoAnalysisViewSet removed
# router.register(r'video-analysis', views.VideoAnalysisViewSet, basename='video-analysis')

# Define URL patterns
urlpatterns = [
    # Frontend Template Views
    path('', views.welcome_view, name='home'),
    path('home/', views.welcome_view, name='welcome'),
    path('index/', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('camera-feeds/', views.camera_feeds_view, name='camera-feeds'),
    path('incident-history/', views.incident_history_view, name='incident-history'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('emergency-contacts/', views.emergency_contacts_view, name='emergency-contacts'),
    path('reports/', views.reports_view, name='reports'),
    path('launch/', views.launch_view, name='launch'),
    path('video-recordings/', views.video_recordings_view, name='video-recordings'),
    path('video-upload/', views.video_upload_view, name='video-upload'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/analytics-data/', views.analytics_data, name='analytics-data'),
    
    # Real-time analysis endpoints
    path('api/analyze-video/', views.analyze_video_realtime, name='analyze-video'),
    path('api/confidence-live/', views.get_video_confidence_live, name='confidence-live'),
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard-stats'),
    
    # Real AI Detection endpoints
    path('api/real-ai-detection-live/', views.real_ai_detection_live, name='real_ai_detection_live'),
    path('api/ai-detection-capabilities/', views.real_ai_detection_live, name='ai_detection_capabilities'),
    
    # Download and Report endpoints
    path('api/download-snapshot/<int:incident_id>/', views.download_incident_snapshot, name='download_incident_snapshot'),
    path('api/generate-report/<int:incident_id>/', views.generate_incident_report, name='generate_incident_report'),
    
    # Additional custom endpoints can be added here
]

# Router URLs will create the following endpoints:
# 
# Fire Detection:
# GET    /api/fire-detection/                 - List all fire events
# POST   /api/fire-detection/                 - Create fire event
# GET    /api/fire-detection/{id}/            - Get specific fire event
# PUT    /api/fire-detection/{id}/            - Update fire event
# DELETE /api/fire-detection/{id}/            - Delete fire event
# POST   /api/fire-detection/detect_fire/     - Process camera frame
# POST   /api/fire-detection/{id}/resolve_incident/ - Resolve incident
# POST   /api/fire-detection/{id}/mark_false_alarm/ - Mark false alarm
# GET    /api/fire-detection/recent_incidents/ - Get recent incidents
# GET    /api/fire-detection/statistics/      - Get statistics
#
# Cameras:
# GET    /api/cameras/                        - List all cameras
# POST   /api/cameras/                        - Create camera
# GET    /api/cameras/{id}/                   - Get specific camera
# PUT    /api/cameras/{id}/                   - Update camera
# DELETE /api/cameras/{id}/                   - Delete camera
# POST   /api/cameras/{id}/start_recording/   - Start recording
# POST   /api/cameras/{id}/stop_recording/    - Stop recording
# POST   /api/cameras/start_all/              - Start all cameras
# POST   /api/cameras/stop_all/               - Stop all cameras
# POST   /api/cameras/{id}/test_connection/   - Test camera connection
#
# Emergency Contacts:
# GET    /api/emergency-contacts/             - List all contacts
# POST   /api/emergency-contacts/             - Create contact
# GET    /api/emergency-contacts/{id}/        - Get specific contact
# PUT    /api/emergency-contacts/{id}/        - Update contact
# DELETE /api/emergency-contacts/{id}/        - Delete contact
# POST   /api/emergency-contacts/test_all_contacts/ - Test all contacts
# POST   /api/emergency-contacts/emergency_alert/ - Send emergency alert
#
# System Configuration:
# GET    /api/system-config/                  - List configuration
# POST   /api/system-config/                  - Create/Update configuration
# GET    /api/system-config/{id}/             - Get configuration
# PUT    /api/system-config/{id}/             - Update configuration
# GET    /api/system-config/current_config/   - Get current config
# POST   /api/system-config/update_config/    - Update config
