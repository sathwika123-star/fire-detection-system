# Fire Detection App Admin Configuration
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Camera, FireDetectionEvent, EmergencyContact, 
    SystemConfiguration, AlertNotification, SystemPerformanceMetrics
)

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    """Admin interface for Camera model"""
    
    list_display = [
        'name', 'location', 'status_badge', 'is_recording', 
        'resolution', 'created_at'
    ]
    list_filter = ['status', 'is_recording', 'resolution', 'created_at']
    search_fields = ['name', 'location', 'rtsp_url']
    list_editable = ['is_recording', 'resolution']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location')
        }),
        ('Network Configuration', {
            'fields': ('rtsp_url',)
        }),
        ('Camera Settings', {
            'fields': ('status', 'resolution', 'is_recording')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['start_recording', 'stop_recording']
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'online': 'green',
            'offline': 'red',
            'maintenance': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def start_recording(self, request, queryset):
        """Admin action to start recording for selected cameras"""
        updated = queryset.update(is_recording=True)
        self.message_user(request, f'Started recording for {updated} cameras.')
    start_recording.short_description = 'Start recording for selected cameras'
    
    def stop_recording(self, request, queryset):
        """Admin action to stop recording for selected cameras"""
        updated = queryset.update(is_recording=False)
        self.message_user(request, f'Stopped recording for {updated} cameras.')
    stop_recording.short_description = 'Stop recording for selected cameras'

@admin.register(FireDetectionEvent)
class FireDetectionEventAdmin(admin.ModelAdmin):
    """Admin interface for FireDetectionEvent model"""
    
    list_display = [
        'id', 'camera_link', 'detection_type', 'detected_at', 'confidence_badge', 
        'severity', 'status_badge', 'resolved_at'
    ]
    list_filter = [
        'detection_type', 'severity', 'status', 'camera', 'detected_at', 'confidence_score'
    ]
    search_fields = ['camera__name', 'camera__location', 'notes']
    readonly_fields = ['detected_at', 'created_at']
    date_hierarchy = 'detected_at'
    ordering = ['-detected_at']
    
    fieldsets = (
        ('Detection Information', {
            'fields': ('camera', 'detection_type', 'detected_at', 'confidence_score', 'severity', 'people_count')
        }),
        ('Event Status', {
            'fields': ('status', 'resolved_at', 'notes')
        }),
        ('Additional Information', {
            'fields': ('bounding_boxes', 'snapshot_path'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_resolved', 'mark_false_alarm', 'mark_investigating']
    
    def camera_link(self, obj):
        """Display camera as a clickable link"""
        url = reverse('admin:fire_detection_camera_change', args=[obj.camera.pk])
        return format_html('<a href="{}">{}</a>', url, obj.camera.name)
    camera_link.short_description = 'Camera'
    
    def confidence_badge(self, obj):
        """Display confidence with color coding"""
        if obj.confidence_score >= 0.8:
            color = 'green'
        elif obj.confidence_score >= 0.6:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1%}</span>',
            color,
            obj.confidence_score
        )
    confidence_badge.short_description = 'Confidence'
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'active': 'red',
            'investigating': 'orange',
            'resolved': 'green',
            'false_alarm': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def response_time_display(self, obj):
        """Display response time in minutes"""
        if obj.response_time:
            minutes = obj.response_time.total_seconds() / 60
            return f"{minutes:.1f} min"
        return "-"
    response_time_display.short_description = 'Response Time'
    
    def mark_resolved(self, request, queryset):
        """Admin action to mark incidents as resolved"""
        now = timezone.now()
        for event in queryset:
            if event.status == 'active':
                event.status = 'resolved'
                event.resolved_at = now
                if event.detected_at:
                    event.response_time = now - event.detected_at
                event.save()
        
        count = queryset.filter(status='resolved').count()
        self.message_user(request, f'Marked {count} incidents as resolved.')
    mark_resolved.short_description = 'Mark selected incidents as resolved'
    
    def mark_false_alarm(self, request, queryset):
        """Admin action to mark incidents as false alarms"""
        updated = queryset.update(
            status='false_alarm',
            resolved_at=timezone.now()
        )
        self.message_user(request, f'Marked {updated} incidents as false alarms.')
    mark_false_alarm.short_description = 'Mark selected incidents as false alarms'
    
    def mark_investigating(self, request, queryset):
        """Admin action to mark incidents as under investigation"""
        updated = queryset.update(status='investigating')
        self.message_user(request, f'Marked {updated} incidents as under investigation.')
    mark_investigating.short_description = 'Mark selected incidents as investigating'

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Admin interface for EmergencyContact model"""
    
    list_display = [
        'name', 'title', 'phone', 'email', 'category_badge', 
        'priority', 'availability_badge', 'created_at'
    ]
    list_filter = ['category', 'priority', 'is_available', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = []
    ordering = ['priority', 'category', 'name']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'title', 'phone', 'email')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at']
    actions = ['mark_available', 'mark_unavailable', 'test_contacts']
    
    def category_badge(self, obj):
        """Display category with styling"""
        colors = {
            'fire_department': 'red',
            'police': 'blue',
            'medical': 'green',
            'security': 'orange',
            'management': 'purple',
            'emergency_services': 'darkred'
        }
        color = colors.get(obj.category, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_category_display()
        )
    category_badge.short_description = 'Category'
    
    def priority_badge(self, obj):
        """Display priority with color coding"""
        colors = {
            'high': 'red',
            'medium': 'orange',
            'low': 'green'
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.priority.title()
        )
    priority_badge.short_description = 'Priority'
    
    def availability_badge(self, obj):
        """Display availability status"""
        if obj.is_available:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Available</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Unavailable</span>'
            )
    availability_badge.short_description = 'Availability'
    
    def mark_available(self, request, queryset):
        """Admin action to mark contacts as available"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f'Marked {updated} contacts as available.')
    mark_available.short_description = 'Mark selected contacts as available'
    
    def mark_unavailable(self, request, queryset):
        """Admin action to mark contacts as unavailable"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f'Marked {updated} contacts as unavailable.')
    mark_unavailable.short_description = 'Mark selected contacts as unavailable'
    
    def test_contacts(self, request, queryset):
        """Admin action to test emergency contacts"""
        # This would integrate with your notification system
        count = queryset.count()
        self.message_user(
            request, 
            f'Testing notification system for {count} contacts. Check logs for results.'
        )
    test_contacts.short_description = 'Test selected emergency contacts'

@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for SystemConfiguration model"""
    
    list_display = [
        'id', 'detection_threshold', 'auto_alert_threshold',
        'enable_sms_alerts', 'enable_email_alerts', 'updated_at'
    ]
    
    fieldsets = (
        ('Detection Settings', {
            'fields': (
                'detection_threshold',
                'auto_alert_threshold',
                'consecutive_frames_required'
            )
        }),
        ('Emergency Response Settings', {
            'fields': (
                'enable_sms_alerts',
                'enable_email_alerts',
                'enable_siren',
                'siren_duration'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        """Only allow one configuration instance"""
        return not SystemConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of configuration"""
        return False

@admin.register(AlertNotification)
class AlertNotificationAdmin(admin.ModelAdmin):
    """Admin interface for AlertNotification model"""
    
    list_display = [
        'id', 'notification_type', 'recipient_contact', 'status_badge',
        'urgency_badge', 'sent_at', 'delivered_at'
    ]
    list_filter = ['notification_type', 'status', 'urgency_level', 'sent_at']
    search_fields = ['recipient_contact', 'message_title', 'message_body']
    readonly_fields = ['sent_at', 'delivered_at', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('notification_type', 'recipient_contact', 'urgency_level')
        }),
        ('Message Content', {
            'fields': ('message_title', 'message_body')
        }),
        ('Status & Timing', {
            'fields': ('status', 'sent_at', 'delivered_at')
        }),
        ('Related Event', {
            'fields': ('fire_event',)
        })
    )
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': 'orange',
            'sent': 'blue',
            'delivered': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def urgency_badge(self, obj):
        """Display urgency with color coding"""
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'critical': 'darkred'
        }
        color = colors.get(obj.urgency_level, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_urgency_level_display()
        )
    urgency_badge.short_description = 'Urgency'

@admin.register(SystemPerformanceMetrics)
class SystemPerformanceMetricsAdmin(admin.ModelAdmin):
    """Admin interface for SystemPerformanceMetrics model"""
    
    list_display = [
        'measurement_time', 'cpu_usage_display', 'memory_usage_display',
        'active_cameras_count', 'fps_display', 'detections_per_minute'
    ]
    list_filter = ['measurement_time', 'active_cameras_count']
    readonly_fields = ['measurement_time']
    ordering = ['-measurement_time']
    
    def cpu_usage_display(self, obj):
        """Display CPU usage with color coding"""
        if obj.cpu_usage_percentage is None:
            return "-"
        
        if obj.cpu_usage_percentage > 80:
            color = 'red'
        elif obj.cpu_usage_percentage > 60:
            color = 'orange'
        else:
            color = 'green'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            obj.cpu_usage_percentage
        )
    cpu_usage_display.short_description = 'CPU Usage'
    
    def memory_usage_display(self, obj):
        """Display memory usage with color coding"""
        if obj.memory_usage_percentage is None:
            return "-"
        
        if obj.memory_usage_percentage > 80:
            color = 'red'
        elif obj.memory_usage_percentage > 60:
            color = 'orange'
        else:
            color = 'green'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            obj.memory_usage_percentage
        )
    memory_usage_display.short_description = 'Memory Usage'
    
    def fps_display(self, obj):
        """Display FPS with formatting"""
        if obj.frames_per_second is None:
            return "-"
        return f"{obj.frames_per_second:.1f} FPS"
    fps_display.short_description = 'Frame Rate'

# Customize admin site headers
admin.site.site_header = "Fire Detection System Administration"
admin.site.site_title = "Fire Detection Admin"
admin.site.index_title = "Welcome to Fire Detection System Administration"
