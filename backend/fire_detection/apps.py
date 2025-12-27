# Fire Detection Django App Configuration
from django.apps import AppConfig

class FireDetectionConfig(AppConfig):
    """
    Configuration for the Fire Detection app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fire_detection'
    verbose_name = 'Fire Detection System'
    
    def ready(self):
        """
        Called when Django starts up
        Perform any initialization needed for the app
        """
        import logging
        
        # Set up logging for the fire detection app
        logger = logging.getLogger(__name__)
        logger.info("Fire Detection System app is ready")
        
        # Import signal handlers (if you add any)
        try:
            from . import signals
        except ImportError:
            pass  # No signals defined yet
        
        # Initialize any background services (if needed)
        # This could include starting camera monitoring, etc.
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize background services for fire detection"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # You can add any initialization code here
            # For example, checking camera connections, loading AI models, etc.
            logger.info("Fire detection services initialized")
        except Exception as e:
            logger.error(f"Failed to initialize fire detection services: {e}")

# Default configuration - this tells Django about our app
default_app_config = 'fire_detection.apps.FireDetectionConfig'
