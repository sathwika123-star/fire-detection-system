# Main URL configuration for Fire Detection Backend
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Fire Detection app URLs (includes frontend and API)
    path('', include('fire_detection.urls')),
    
    # DRF Browsable API authentication
    path('api-auth/', include('rest_framework.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Serve videos folder
    urlpatterns += static(settings.VIDEOS_URL, document_root=settings.VIDEOS_ROOT)
