# Fire Detection App - Serializers
from rest_framework import serializers
from .models import Camera, FireDetectionEvent, EmergencyContact, SystemConfiguration

class CameraSerializer(serializers.ModelSerializer):
    last_detection = serializers.SerializerMethodField()
    total_detections = serializers.SerializerMethodField()
    
    class Meta:
        model = Camera
        fields = [
            'id', 'name', 'location', 'ip_address', 'port', 'username', 
            'password', 'rtsp_url', 'status', 'is_recording', 'is_detection_enabled',
            'detection_sensitivity', 'created_at', 'updated_at',
            'last_detection', 'total_detections'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_last_detection(self, obj):
        """Get the timestamp of the last fire detection for this camera"""
        last_event = obj.fire_events.order_by('-detected_at').first()
        return last_event.detected_at if last_event else None
    
    def get_total_detections(self, obj):
        """Get total number of fire detections for this camera"""
        return obj.fire_events.count()

class FireDetectionEventSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    camera_location = serializers.CharField(source='camera.location', read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = FireDetectionEvent
        fields = [
            'id', 'camera', 'camera_name', 'camera_location', 'detected_at',
            'confidence_score', 'bounding_box', 'image_url', 'status',
            'resolved_at', 'response_time', 'notes', 'false_alarm_reason',
            'duration_minutes'
        ]
    
    def get_duration_minutes(self, obj):
        """Calculate duration in minutes if resolved"""
        if obj.resolved_at and obj.detected_at:
            duration = obj.resolved_at - obj.detected_at
            return round(duration.total_seconds() / 60, 2)
        return None

class EmergencyContactSerializer(serializers.ModelSerializer):
    full_contact_info = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'name', 'title', 'phone', 'email', 'category', 'priority',
            'is_available', 'created_at',
            'full_contact_info'
        ]
    
    def get_full_contact_info(self, obj):
        """Get formatted contact information"""
        return {
            'display_name': f"{obj.name} ({obj.get_category_display()})",
            'contact_methods': {
                'phone': obj.phone,
                'email': obj.email
            },
            'priority_level': obj.priority.upper() if obj.priority else 'MEDIUM',
            'availability': 'Available' if obj.is_available else 'Unavailable'
        }

class SystemConfigurationSerializer(serializers.ModelSerializer):
    detection_areas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemConfiguration
        fields = [
            'id', 'detection_confidence_threshold', 'alert_cooldown_minutes',
            'auto_emergency_call', 'emergency_call_delay_seconds',
            'sms_notifications_enabled', 'email_notifications_enabled',
            'fire_department_number', 'system_admin_email',
            'detection_areas', 'notification_sound_enabled',
            'max_false_alarms_per_day', 'system_maintenance_mode',
            'updated_at', 'detection_areas_count'
        ]
    
    def get_detection_areas_count(self, obj):
        """Get number of detection areas configured"""
        if obj.detection_areas and isinstance(obj.detection_areas, list):
            return len(obj.detection_areas)
        return 0
    
    def validate_detection_confidence_threshold(self, value):
        """Validate confidence threshold is between 0 and 1"""
        if not 0 <= value <= 1:
            raise serializers.ValidationError(
                "Detection confidence threshold must be between 0 and 1"
            )
        return value
    
    def validate_alert_cooldown_minutes(self, value):
        """Validate alert cooldown is positive"""
        if value < 0:
            raise serializers.ValidationError(
                "Alert cooldown minutes must be positive"
            )
        return value
    
    def validate_emergency_call_delay_seconds(self, value):
        """Validate emergency call delay is reasonable"""
        if not 0 <= value <= 300:  # Max 5 minutes
            raise serializers.ValidationError(
                "Emergency call delay must be between 0 and 300 seconds"
            )
        return value
    
    def validate_max_false_alarms_per_day(self, value):
        """Validate max false alarms is reasonable"""
        if value < 1:
            raise serializers.ValidationError(
                "Max false alarms per day must be at least 1"
            )
        return value

# Additional serializers for specific use cases

class CameraSummarySerializer(serializers.ModelSerializer):
    """Lightweight camera serializer for lists and summaries"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Camera
        fields = ['id', 'name', 'location', 'status', 'status_display', 'is_recording']

class RecentFireEventSerializer(serializers.ModelSerializer):
    """Serializer for recent fire events with minimal data"""
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = FireDetectionEvent
        fields = [
            'id', 'camera_name', 'detected_at', 'confidence_score', 
            'status', 'time_ago'
        ]
    
    def get_time_ago(self, obj):
        """Get human-readable time since detection"""
        from django.utils import timezone
        import datetime
        
        now = timezone.now()
        diff = now - obj.detected_at
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"

class EmergencyContactSummarySerializer(serializers.ModelSerializer):
    """Lightweight emergency contact serializer"""
    
    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'phone', 'category', 'priority', 'is_available']

class FireDetectionStatsSerializer(serializers.Serializer):
    """Serializer for fire detection statistics"""
    total_incidents = serializers.IntegerField()
    incidents_today = serializers.IntegerField()
    incidents_this_week = serializers.IntegerField()
    incidents_this_month = serializers.IntegerField()
    false_alarms = serializers.IntegerField()
    average_confidence = serializers.FloatField()
    average_response_time = serializers.DurationField()
    active_cameras = serializers.IntegerField(required=False)
    system_uptime = serializers.CharField(required=False)
