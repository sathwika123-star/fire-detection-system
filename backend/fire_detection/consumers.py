# Fire Detection App - WebSocket Consumers
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class FireDetectionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time fire detection updates
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.room_name = "fire_detection"
        self.room_group_name = f"fire_detection_{self.room_name}"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial system status
        await self.send_system_status()
        
        logger.info(f"WebSocket connected: {self.channel_name}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"WebSocket disconnected: {self.channel_name} (code: {close_code})")
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': timezone.now().isoformat()
                }))
            
            elif message_type == 'request_status':
                await self.send_system_status()
            
            elif message_type == 'camera_feed':
                # Handle camera feed data for processing
                camera_id = text_data_json.get('camera_id')
                frame_data = text_data_json.get('frame_data')
                
                if camera_id and frame_data:
                    await self.process_camera_frame(camera_id, frame_data)
            
            elif message_type == 'emergency_action':
                action = text_data_json.get('action')
                await self.handle_emergency_action(action, text_data_json)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from WebSocket")
        except Exception as e:
            logger.error(f"WebSocket receive error: {str(e)}")
    
    async def send_system_status(self):
        """Send current system status to client"""
        try:
            status = await self.get_system_status()
            await self.send(text_data=json.dumps({
                'type': 'system_status',
                'data': status,
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending system status: {str(e)}")
    
    async def process_camera_frame(self, camera_id, frame_data):
        """Process camera frame for fire detection"""
        try:
            from .tasks import process_camera_frame
            
            # Process frame asynchronously
            task = await database_sync_to_async(process_camera_frame.delay)(
                camera_id, frame_data
            )
            
            await self.send(text_data=json.dumps({
                'type': 'frame_processed',
                'camera_id': camera_id,
                'task_id': task.id,
                'timestamp': timezone.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error processing camera frame: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Frame processing failed',
                'timestamp': timezone.now().isoformat()
            }))
    
    async def handle_emergency_action(self, action, data):
        """Handle emergency actions from client"""
        try:
            if action == 'alert_all':
                incident_id = data.get('incident_id')
                message = data.get('message', 'Emergency fire alert')
                
                if incident_id:
                    from .tasks import send_emergency_alerts
                    task = await database_sync_to_async(send_emergency_alerts.delay)(
                        incident_id, message
                    )
                    
                    await self.send(text_data=json.dumps({
                        'type': 'emergency_alert_sent',
                        'incident_id': incident_id,
                        'task_id': task.id,
                        'timestamp': timezone.now().isoformat()
                    }))
            
            elif action == 'resolve_incident':
                incident_id = data.get('incident_id')
                if incident_id:
                    await self.resolve_incident(incident_id)
            
        except Exception as e:
            logger.error(f"Error handling emergency action: {str(e)}")
    
    @database_sync_to_async
    def get_system_status(self):
        """Get current system status from database"""
        from .models import Camera, FireDetectionEvent, SystemConfiguration
        from django.db.models import Count
        
        config = SystemConfiguration.get_config()
        cameras = Camera.objects.all()
        
        # Get recent incidents (last 24 hours)
        from datetime import timedelta
        recent_incidents = FireDetectionEvent.objects.filter(
            detected_at__gte=timezone.now() - timedelta(hours=24)
        )
        
        return {
            'total_cameras': cameras.count(),
            'online_cameras': cameras.filter(status='online').count(),
            'recording_cameras': cameras.filter(is_recording=True).count(),
            'active_incidents': FireDetectionEvent.objects.filter(status='active').count(),
            'recent_incidents': recent_incidents.count(),
            'system_maintenance': config.system_maintenance_mode,
            'detection_enabled': not config.system_maintenance_mode,
            'cameras': [
                {
                    'id': cam.id,
                    'name': cam.name,
                    'location': cam.location,
                    'status': cam.status,
                    'is_recording': cam.is_recording
                }
                for cam in cameras
            ]
        }
    
    @database_sync_to_async
    def resolve_incident(self, incident_id):
        """Resolve a fire incident"""
        from .models import FireDetectionEvent
        
        try:
            incident = FireDetectionEvent.objects.get(id=incident_id)
            incident.status = 'resolved'
            incident.resolved_at = timezone.now()
            
            if incident.detected_at:
                incident.response_time = incident.resolved_at - incident.detected_at
            
            incident.save()
            
            return True
        except FireDetectionEvent.DoesNotExist:
            return False
    
    # Event handlers for group messages
    async def fire_detected(self, event):
        """Send fire detection alert to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'fire_detected',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))
    
    async def incident_resolved(self, event):
        """Send incident resolution to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'incident_resolved',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))
    
    async def camera_status_update(self, event):
        """Send camera status update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'camera_status_update',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))
    
    async def system_alert(self, event):
        """Send system alert to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'system_alert',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))

class CameraFeedConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for camera feed streaming
    """
    
    async def connect(self):
        """Handle camera feed connection"""
        self.camera_id = self.scope['url_route']['kwargs']['camera_id']
        self.room_group_name = f"camera_feed_{self.camera_id}"
        
        # Join camera feed group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Camera feed connected: camera_{self.camera_id}")
    
    async def disconnect(self, close_code):
        """Handle camera feed disconnection"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Camera feed disconnected: camera_{self.camera_id}")
    
    async def receive(self, text_data):
        """Handle camera feed data"""
        try:
            data = json.loads(text_data)
            
            if data.get('type') == 'frame':
                # Process incoming frame
                frame_data = data.get('frame_data')
                if frame_data:
                    await self.process_frame(frame_data)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from camera feed")
        except Exception as e:
            logger.error(f"Camera feed receive error: {str(e)}")
    
    async def process_frame(self, frame_data):
        """Process camera frame"""
        try:
            from .tasks import process_camera_frame
            
            # Process frame for fire detection
            task = await database_sync_to_async(process_camera_frame.delay)(
                self.camera_id, frame_data
            )
            
            # Broadcast frame to other clients (optional)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'frame_update',
                    'frame_data': frame_data,
                    'camera_id': self.camera_id
                }
            )
            
        except Exception as e:
            logger.error(f"Frame processing error: {str(e)}")
    
    async def frame_update(self, event):
        """Send frame update to clients"""
        await self.send(text_data=json.dumps({
            'type': 'frame_update',
            'camera_id': event['camera_id'],
            'frame_data': event['frame_data'],
            'timestamp': timezone.now().isoformat()
        }))

class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for dashboard real-time updates
    """
    
    async def connect(self):
        """Handle dashboard connection"""
        self.room_group_name = "dashboard_updates"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial dashboard data
        await self.send_dashboard_data()
        
        logger.info(f"Dashboard connected: {self.channel_name}")
    
    async def disconnect(self, close_code):
        """Handle dashboard disconnection"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Dashboard disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Handle dashboard requests"""
        try:
            data = json.loads(text_data)
            request_type = data.get('type')
            
            if request_type == 'refresh_data':
                await self.send_dashboard_data()
            
            elif request_type == 'get_analytics':
                period = data.get('period', '24h')
                await self.send_analytics_data(period)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from dashboard")
        except Exception as e:
            logger.error(f"Dashboard receive error: {str(e)}")
    
    async def send_dashboard_data(self):
        """Send current dashboard data"""
        try:
            data = await self.get_dashboard_data()
            await self.send(text_data=json.dumps({
                'type': 'dashboard_data',
                'data': data,
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending dashboard data: {str(e)}")
    
    async def send_analytics_data(self, period):
        """Send analytics data for specified period"""
        try:
            data = await self.get_analytics_data(period)
            await self.send(text_data=json.dumps({
                'type': 'analytics_data',
                'data': data,
                'period': period,
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending analytics data: {str(e)}")
    
    @database_sync_to_async
    def get_dashboard_data(self):
        """Get dashboard data from database"""
        from .models import Camera, FireDetectionEvent, SystemConfiguration
        from datetime import timedelta
        
        now = timezone.now()
        today = now.date()
        
        # Get system statistics
        total_cameras = Camera.objects.count()
        online_cameras = Camera.objects.filter(status='online').count()
        active_incidents = FireDetectionEvent.objects.filter(status='active').count()
        
        # Get recent incidents
        recent_incidents = FireDetectionEvent.objects.filter(
            detected_at__date=today
        ).order_by('-detected_at')[:5]
        
        return {
            'system_stats': {
                'total_cameras': total_cameras,
                'online_cameras': online_cameras,
                'offline_cameras': total_cameras - online_cameras,
                'active_incidents': active_incidents,
                'incidents_today': recent_incidents.count()
            },
            'recent_incidents': [
                {
                    'id': incident.id,
                    'camera_name': incident.camera.name,
                    'location': incident.camera.location,
                    'detected_at': incident.detected_at.isoformat(),
                    'confidence': incident.confidence_score,
                    'status': incident.status
                }
                for incident in recent_incidents
            ]
        }
    
    @database_sync_to_async
    def get_analytics_data(self, period):
        """Get analytics data for specified period"""
        from .models import FireDetectionEvent
        from datetime import timedelta
        from django.db.models import Count, Avg, Q
        
        now = timezone.now()
        
        # Determine time range based on period
        if period == '1h':
            start_time = now - timedelta(hours=1)
        elif period == '24h':
            start_time = now - timedelta(hours=24)
        elif period == '7d':
            start_time = now - timedelta(days=7)
        elif period == '30d':
            start_time = now - timedelta(days=30)
        else:
            start_time = now - timedelta(hours=24)
        
        # Get incidents in time range
        incidents = FireDetectionEvent.objects.filter(
            detected_at__gte=start_time
        )
        
        # Calculate statistics
        stats = incidents.aggregate(
            total_incidents=Count('id'),
            avg_confidence=Avg('confidence_score'),
            false_alarms=Count('id', filter=Q(status='false_alarm'))
        )
        
        return {
            'period': period,
            'total_incidents': stats['total_incidents'] or 0,
            'average_confidence': stats['avg_confidence'] or 0,
            'false_alarms': stats['false_alarms'] or 0,
            'accuracy_rate': (
                (stats['total_incidents'] - stats['false_alarms']) / stats['total_incidents'] * 100
                if stats['total_incidents'] else 100
            )
        }
    
    # Event handlers
    async def dashboard_update(self, event):
        """Send dashboard update"""
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))
    
    async def incident_update(self, event):
        """Send incident update"""
        await self.send(text_data=json.dumps({
            'type': 'incident_update',
            'data': event['data'],
            'timestamp': timezone.now().isoformat()
        }))
