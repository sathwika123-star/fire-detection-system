# Fire Detection System - Django Models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

def generate_uuid():
    """Generate UUID as string without hyphens for primary key (fits in 32 chars)"""
    return str(uuid.uuid4()).replace('-', '')

class Camera(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]
    
    RESOLUTION_CHOICES = [
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4K', '4K'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    rtsp_url = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    resolution = models.CharField(max_length=10, choices=RESOLUTION_CHOICES, default='1080p')
    is_recording = models.BooleanField(default=False)
    last_frame_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fire_detection_camera'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class FireDetectionEvent(models.Model):
    DETECTION_TYPE_CHOICES = [
        ('fire', 'Fire'),
        ('smoke', 'Smoke'),
        ('heat', 'Heat'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=generate_uuid)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='camera_id')
    detection_type = models.CharField(max_length=20, choices=DETECTION_TYPE_CHOICES, default='fire')
    confidence_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    people_count = models.IntegerField(default=0)
    bounding_boxes = models.TextField(default='[]')
    snapshot_path = models.CharField(max_length=500, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fire_detection_firedetectionevent'
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.detection_type.title()} - {self.camera.name} - {self.confidence_score:.2f}"

class EmergencyContact(models.Model):
    CATEGORY_CHOICES = [
        ('fire_department', 'Fire Department'),
        ('medical', 'Medical'),
        ('police', 'Police'),
        ('security', 'Security'),
        ('management', 'Management'),
    ]
    
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, default='medium')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fire_detection_emergencycontact'
        ordering = ['priority', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.title}"

class SystemConfiguration(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    detection_threshold = models.FloatField(default=0.5)
    auto_alert_threshold = models.FloatField(default=0.8)
    consecutive_frames_required = models.IntegerField(default=3)
    enable_sms_alerts = models.BooleanField(default=True)
    enable_email_alerts = models.BooleanField(default=True)
    enable_siren = models.BooleanField(default=True)
    siren_duration = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fire_detection_systemconfiguration'
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"
    
    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(id=1)
        return config
    
    def __str__(self):
        return "System Configuration"

class AlertNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('call', 'Call'),
        ('push', 'Push'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    fire_event = models.ForeignKey(FireDetectionEvent, on_delete=models.CASCADE, null=True, blank=True, db_column='fire_event_id')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES)
    recipient_contact = models.CharField(max_length=200)
    message_title = models.CharField(max_length=200)
    message_body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'alert_notifications'
        ordering = ['-created_at']

class SystemPerformanceMetrics(models.Model):
    cpu_usage_percentage = models.FloatField(null=True, blank=True)
    memory_usage_percentage = models.FloatField(null=True, blank=True)
    active_cameras_count = models.IntegerField(default=0)
    frames_per_second = models.FloatField(null=True, blank=True)
    detections_per_minute = models.FloatField(default=0)
    measurement_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'system_performance_metrics'
        ordering = ['-measurement_time']

