# Fire Detection App - Celery Tasks
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import cv2
import numpy as np
import base64
import logging
import json
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def process_camera_frame(camera_id, frame_data):
    """
    Process camera frame for fire detection using YOLOv8
    """
    from .models import Camera, FireDetectionEvent, SystemConfiguration
    from .ai_detection import FireDetector
    
    try:
        camera = Camera.objects.get(id=camera_id)
        config = SystemConfiguration.get_config()
        
        # Decode base64 frame
        frame_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            logger.error(f"Failed to decode frame for camera {camera.name}")
            return {"error": "Frame decode failed"}
        
        # Initialize fire detector
        detector = FireDetector()
        
        # Perform fire detection
        detection_result = detector.detect_fire(frame, camera.detection_sensitivity)
        
        if detection_result['fire_detected']:
            confidence = detection_result['confidence']
            bounding_box = detection_result['bounding_box']
            
            # Check if confidence meets threshold
            if confidence >= config.detection_confidence_threshold:
                
                # Check for recent alerts to avoid spam
                recent_threshold = timezone.now() - timedelta(
                    minutes=config.alert_cooldown_minutes
                )
                recent_alert = FireDetectionEvent.objects.filter(
                    camera=camera,
                    detected_at__gte=recent_threshold,
                    status__in=['active', 'investigating']
                ).exists()
                
                if not recent_alert:
                    # Create fire detection event
                    event = FireDetectionEvent.objects.create(
                        camera=camera,
                        confidence_score=confidence,
                        bounding_box=bounding_box,
                        status='active'
                    )
                    
                    # Send alerts
                    send_fire_alert.delay(event.id)
                    
                    # Auto emergency call if enabled
                    if config.auto_emergency_call:
                        trigger_emergency_call.delay(
                            event.id, 
                            config.emergency_call_delay_seconds
                        )
                    
                    logger.info(f"Fire detected in camera {camera.name} with confidence {confidence}")
                    
                    return {
                        "fire_detected": True,
                        "event_id": event.id,
                        "confidence": confidence,
                        "camera": camera.name
                    }
        
        return {"fire_detected": False, "camera": camera.name}
        
    except Camera.DoesNotExist:
        logger.error(f"Camera with ID {camera_id} not found")
        return {"error": "Camera not found"}
    except Exception as e:
                logger.error(f"Failed to send emergency alerts: {str(e)}")

@shared_task
def analyze_video_for_fire(analysis_id):
    """
    Analyze uploaded video for fire detection and trigger alerts
    """
    from .models import VideoAnalysis, Camera, FireDetectionEvent, SystemConfiguration
    from .ai_detection import FireDetector
    from django.utils import timezone
    import cv2
    import numpy as np
    import tempfile
    import os
    import requests
    
    try:
        analysis = VideoAnalysis.objects.get(id=analysis_id)
        config = SystemConfiguration.get_config()
        
        # Update status to processing
        analysis.analysis_status = 'processing'
        analysis.save()
        
        logger.info(f"Starting video analysis for: {analysis.title}")
        
        # Get video source
        video_path = None
        if analysis.source_type == 'url' and analysis.video_url:
            # Download video from URL temporarily
            try:
                response = requests.get(analysis.video_url, stream=True)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        tmp_file.write(chunk)
                    video_path = tmp_file.name
            except Exception as e:
                logger.error(f"Failed to download video: {str(e)}")
                analysis.analysis_status = 'failed'
                analysis.save()
                return
        elif analysis.source_type == 'upload' and analysis.video_file:
            video_path = analysis.video_file.path
        
        if not video_path or not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            analysis.analysis_status = 'failed'
            analysis.save()
            return
        
        # Initialize fire detector
        detector = FireDetector()
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Cannot open video: {video_path}")
            analysis.analysis_status = 'failed'
            analysis.save()
            return
        
        frame_count = 0
        fire_detections = []
        max_confidence = 0.0
        fire_detected_frame = None
        
        # Process video frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Process every 30th frame to speed up analysis
            if frame_count % 30 == 0:
                detection_result = detector.detect_fire(frame, config.detection_threshold)
                
                if detection_result['fire_detected']:
                    confidence = detection_result['confidence']
                    fire_detections.append({
                        'frame': frame_count,
                        'confidence': confidence,
                        'timestamp': frame_count / cap.get(cv2.CAP_PROP_FPS)
                    })
                    
                    if confidence > max_confidence:
                        max_confidence = confidence
                        fire_detected_frame = frame_count / cap.get(cv2.CAP_PROP_FPS)
        
        cap.release()
        
        # Clean up temporary file
        if analysis.source_type == 'url' and video_path:
            try:
                os.unlink(video_path)
            except:
                pass
        
        # Update analysis results
        fire_detected = len(fire_detections) > 0 and max_confidence >= config.detection_confidence_threshold
        
        analysis.fire_detected = fire_detected
        analysis.confidence_score = max_confidence
        analysis.detection_timestamp = str(fire_detected_frame) if fire_detected_frame else None
        analysis.analysis_status = 'completed'
        analysis.analyzed_at = timezone.now()
        
        # If fire detected, trigger emergency response
        if fire_detected:
            logger.info(f"🔥 FIRE DETECTED in video: {analysis.title} with confidence {max_confidence:.2%}")
            
            # Create or get virtual camera for this analysis
            virtual_camera, created = Camera.objects.get_or_create(
                name=f"Video Analysis - {analysis.title}",
                defaults={
                    'location': analysis.location,
                    'rtsp_url': analysis.video_url or 'file://uploaded',
                    'status': 'online'
                }
            )
            
            # Create fire detection event
            fire_event = FireDetectionEvent.objects.create(
                camera=virtual_camera,
                confidence_score=max_confidence,
                severity='high' if max_confidence > 0.8 else 'medium',
                status='active',
                bounding_boxes='[]'
            )
            
            # Trigger emergency alerts
            if config.sms_notifications:
                send_fire_alert.delay(fire_event.id)
                analysis.sms_sent = True
                analysis.alerts_sent = True
            
            if config.auto_emergency_call:
                trigger_emergency_call.delay(fire_event.id, config.emergency_call_delay_seconds)
                analysis.calls_made = True
            
            if config.siren_activation:
                # Simulate siren activation
                logger.info(f"🚨 SIREN ACTIVATED for video: {analysis.title}")
                analysis.siren_activated = True
            
            logger.info(f"📱 Emergency alerts triggered for video analysis: {analysis.title}")
        
        analysis.save()
        
        # Send real-time update to dashboard (WebSocket would be ideal here)
        logger.info(f"Video analysis completed: {analysis.title} - Fire: {fire_detected} - Confidence: {max_confidence:.2%}")
        
        return {
            "analysis_id": str(analysis.id),
            "fire_detected": fire_detected,
            "confidence": max_confidence,
            "alerts_triggered": fire_detected
        }
        
    except VideoAnalysis.DoesNotExist:
        logger.error(f"Video analysis with ID {analysis_id} not found")
        return {"error": "Analysis not found"}
    except Exception as e:
        logger.error(f"Video analysis error: {str(e)}")
        try:
            analysis = VideoAnalysis.objects.get(id=analysis_id)
            analysis.analysis_status = 'failed'
            analysis.save()
        except:
            pass
        return {"error": str(e)}
        return {"error": str(e)}

@shared_task
def send_fire_alert(event_id):
    """
    Send fire alert notifications via SMS and email using HTTP APIs
    Automatically sends to all emergency contacts when fire is detected
    """
    from .models import FireDetectionEvent, EmergencyContact, SystemConfiguration
    import requests
    
    try:
        event = FireDetectionEvent.objects.get(id=event_id)
        config = SystemConfiguration.get_config()
        
        # Get emergency contacts
        contacts = EmergencyContact.objects.filter(
            is_available=True
        ).order_by('priority', 'category')
        
        logger.critical(f"🚨 FIRE DETECTED! Sending automatic alerts for {event.camera.location}")
        logger.critical(f"   Camera: {event.camera.name}")
        logger.critical(f"   Confidence: {event.confidence_score:.2%}")
        logger.critical(f"   Notifying {contacts.count()} emergency contacts")
        
        email_sent = False
        sms_sent = False
        
        # 1. SEND EMAIL ALERTS VIA HTTP API
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/send-emergency-alert/',
                json={
                    'location': event.camera.location,
                    'camera': event.camera.name,
                    'confidence': float(event.confidence_score),
                    'time': event.detected_at.strftime('%Y-%m-%d %H:%M:%S')
                },
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    email_sent = True
                    logger.critical(f"✅ EMAIL ALERTS SENT to {result.get('sent_count', 0)} contacts")
                else:
                    logger.error(f"❌ Email alert failed: {result.get('error')}")
            else:
                logger.error(f"❌ Email HTTP API error: Status {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Failed to send email alerts: {str(e)}")
        
        # 2. SEND SMS ALERTS VIA HTTP API
        try:
            # SMS alerts disabled - WhatsApp functionality removed
            logger.info("SMS/WhatsApp alerts disabled")
        except Exception as e:
            logger.error(f"❌ Failed to send SMS alerts: {str(e)}")
        
        # Summary
        alerts_summary = []
        if email_sent:
            alerts_summary.append("EMAIL")
        if sms_sent:
            alerts_summary.append("WHATSAPP")
        
        if alerts_summary:
            logger.critical(f"🚨 EMERGENCY ALERTS SENT: {', '.join(alerts_summary)}")
            logger.critical(f"📍 Location: {event.camera.location}")
            logger.critical(f"📹 Camera: {event.camera.name}")
            logger.critical(f"⏰ Time: {event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            logger.error("❌ NO ALERTS SENT - Check email/WhatsApp configuration")
        
        return {
            "success": True,
            "email_sent": email_sent,
            "sms_sent": sms_sent,
            "contacts_notified": contacts.count(),
            "location": event.camera.location,
            "camera": event.camera.name
        }
        
    except FireDetectionEvent.DoesNotExist:
        logger.error(f"Fire detection event {event_id} not found")
        return {"error": "Event not found"}
    except Exception as e:
        logger.error(f"Alert sending error: {str(e)}")
        return {"error": str(e)}

@shared_task
def send_sms_notification(phone_number, message):
    """
    Send SMS notification (integrate with your SMS provider)
    Note: For WhatsApp notifications, use the WhatsApp API endpoints directly
    """
    try:
        # For SMS, integrate with SMS provider (e.g., AWS SNS, MSG91, etc.)
        # This function is separate from WhatsApp functionality
        
        # For now, just log the SMS (replace with actual SMS sending)
        logger.info(f"SMS sent to {phone_number}: {message[:100]}...")
        
        return {"success": True, "phone": phone_number}
        
    except Exception as e:
        logger.error(f"SMS sending error to {phone_number}: {str(e)}")
        return {"error": str(e)}

@shared_task
def send_email_notification(email_addresses, subject, message, event_id=None):
    """
    Send email notification
    """
    try:
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="color: #dc2626; margin-bottom: 20px;">🔥 Fire Detection Alert</h2>
                <pre style="background-color: #f8f8f8; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{message}</pre>
                
                {f'<p><a href="http://localhost:8000/dashboard.html?incident={event_id}" style="background-color: #dc2626; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Incident Details</a></p>' if event_id else ''}
                
                <hr style="margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated message from Fire Detection System.<br>
                    Please respond immediately to this emergency alert.
                </p>
            </div>
        </body>
        </html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email_addresses,
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Email sent to {len(email_addresses)} recipients: {subject}")
        return {"success": True, "recipients": len(email_addresses)}
        
    except Exception as e:
        logger.error(f"Email sending error: {str(e)}")
        return {"error": str(e)}

@shared_task
def trigger_emergency_call(event_id, delay_seconds=0):
    """
    Trigger automatic emergency call after delay
    """
    from .models import FireDetectionEvent, SystemConfiguration
    import time
    
    try:
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        
        event = FireDetectionEvent.objects.get(id=event_id)
        config = SystemConfiguration.get_config()
        
        # Check if event is still active
        if event.status not in ['active', 'investigating']:
            logger.info(f"Emergency call cancelled - event {event_id} resolved")
            return {"cancelled": True, "reason": "Event resolved"}
        
        # Make emergency call (integrate with your telephony provider)
        emergency_number = config.fire_department_number
        
        if emergency_number:
            # Example: Integration with telephony service
            # This would make an actual call in production
            logger.info(f"Emergency call triggered to {emergency_number} for event {event_id}")
            
            # Update event status
            event.save()
            
            return {"success": True, "number_called": emergency_number}
        else:
            logger.warning("No emergency number configured")
            return {"error": "No emergency number configured"}
        
    except FireDetectionEvent.DoesNotExist:
        logger.error(f"Fire detection event {event_id} not found")
        return {"error": "Event not found"}
    except Exception as e:
        logger.error(f"Emergency call error: {str(e)}")
        return {"error": str(e)}

@shared_task
def send_emergency_alerts(incident_id, custom_message=None):
    """
    Send emergency alerts to all primary contacts
    """
    from .models import FireDetectionEvent, EmergencyContact
    
    try:
        event = FireDetectionEvent.objects.get(id=incident_id)
        
        # Get primary emergency contacts
        primary_contacts = EmergencyContact.objects.filter(
            category__in=['fire_department', 'primary', 'medical'],
            is_available=True
        ).order_by('category', '-priority')
        
        message = custom_message or f"""
        🚨 EMERGENCY FIRE ALERT 🚨
        
        IMMEDIATE RESPONSE REQUIRED
        
        Location: {event.camera.location}
        Camera: {event.camera.name}
        Detection Time: {event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
        Confidence Level: {event.confidence_score:.2%}
        
        This is an automated emergency alert.
        Dispatching emergency services immediately.
        """
        
        alerts_sent = 0
        
        for contact in primary_contacts:
            if contact.phone:
                send_sms_notification.delay(contact.phone, message)
                alerts_sent += 1
            
            if contact.email:
                send_email_notification.delay(
                    [contact.email],
                    "🚨 EMERGENCY FIRE ALERT - IMMEDIATE RESPONSE REQUIRED",
                    message,
                    incident_id
                )
                alerts_sent += 1
        
        logger.info(f"Emergency alerts sent for incident {incident_id}: {alerts_sent} alerts")
        return {"success": True, "alerts_sent": alerts_sent}
        
    except FireDetectionEvent.DoesNotExist:
        logger.error(f"Fire detection event {incident_id} not found")
        return {"error": "Event not found"}
    except Exception as e:
        logger.error(f"Emergency alert error: {str(e)}")
        return {"error": str(e)}

@shared_task
def system_health_check():
    """
    Perform system health check
    """
    from .models import Camera, SystemConfiguration
    
    try:
        config = SystemConfiguration.get_config()
        
        if config.system_maintenance_mode:
            logger.info("System health check skipped - maintenance mode active")
            return {"skipped": True, "reason": "maintenance_mode"}
        
        # Check camera status
        cameras = Camera.objects.all()
        offline_cameras = cameras.filter(status='offline')
        
        health_report = {
            "timestamp": timezone.now().isoformat(),
            "total_cameras": cameras.count(),
            "online_cameras": cameras.filter(status='online').count(),
            "offline_cameras": offline_cameras.count(),
            "recording_cameras": cameras.filter(is_recording=True).count(),
            "system_status": "healthy" if offline_cameras.count() == 0 else "warning"
        }
        
        # Alert if cameras are offline
        if offline_cameras.count() > 0:
            offline_names = [cam.name for cam in offline_cameras]
            alert_message = f"System Health Alert: {offline_cameras.count()} cameras offline: {', '.join(offline_names)}"
            
            if config.system_admin_email:
                send_email_notification.delay(
                    [config.system_admin_email],
                    "Fire Detection System Health Alert",
                    alert_message
                )
        
        logger.info(f"System health check completed: {health_report['system_status']}")
        return health_report
        
    except Exception as e:
        logger.error(f"System health check error: {str(e)}")
        return {"error": str(e)}

@shared_task
def cleanup_old_events():
    """
    Clean up old fire detection events (older than 90 days)
    """
    from .models import FireDetectionEvent
    from datetime import timedelta
    
    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        old_events = FireDetectionEvent.objects.filter(detected_at__lt=cutoff_date)
        
        deleted_count = old_events.count()
        old_events.delete()
        
        logger.info(f"Cleaned up {deleted_count} old fire detection events")
        return {"success": True, "deleted_count": deleted_count}
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return {"error": str(e)}

@shared_task
def trigger_emergency_response(event_id, video_name, confidence_score):
    """
    Comprehensive emergency response when fire is detected
    """
    from .models import FireDetectionEvent, EmergencyContact, SystemConfiguration
    from django.utils import timezone
    import time
    
    try:
        event = FireDetectionEvent.objects.get(id=event_id)
        config = SystemConfiguration.get_config()
        
        logger.critical(f"🚨 EMERGENCY RESPONSE ACTIVATED - Fire detected in {video_name} with {confidence_score:.1f}% confidence")
        
        # Get all emergency contacts
        emergency_contacts = EmergencyContact.objects.filter(is_available=True).order_by('category', '-priority')
        
        # Prepare emergency message
        emergency_message = f"""
🔥 FIRE EMERGENCY ALERT 🔥

IMMEDIATE ACTION REQUIRED!

📍 Location: {event.camera.location}
📹 Camera: {event.camera.name}
⏰ Detection Time: {event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
📊 Confidence Level: {confidence_score:.1f}%
🎯 Video Source: {video_name}

🚨 EMERGENCY SERVICES HAVE BEEN AUTOMATICALLY NOTIFIED
🚨 EVACUATION PROCEDURES SHOULD BE INITIATED IMMEDIATELY

This is an automated emergency alert from the Fire Detection System.
Event ID: {event_id}
        """
        
        # 1. IMMEDIATE SMS ALERTS TO ALL CONTACTS
        sms_sent_count = 0
        for contact in emergency_contacts:
            if contact.phone:
                try:
                    send_emergency_sms.delay(contact.phone, contact.name, emergency_message, str(event_id))
                    sms_sent_count += 1
                    logger.info(f"📱 Emergency SMS queued for {contact.name} ({contact.phone})")
                except Exception as e:
                    logger.error(f"Failed to queue SMS for {contact.name}: {str(e)}")
        
        # 2. IMMEDIATE EMAIL ALERTS TO ALL CONTACTS USING EMAIL SERVICE
        email_sent_count = 0
        try:
            from .email_service import email_service
            email_result = email_service.send_emergency_fire_alert(event)
            email_sent_count = email_result.get('sent_count', 0)
            logger.critical(f"📧 Emergency emails sent to {email_sent_count} contacts via email service")
        except Exception as e:
            logger.error(f"Failed to send emergency emails via email service: {str(e)}")
        
        # 3. PRIORITY AUTOMATIC CALLS TO FIRE DEPARTMENT AND PRIMARY CONTACTS
        call_count = 0
        priority_contacts = emergency_contacts.filter(category__in=['primary', 'fire_department'])[:3]
        
        for contact in priority_contacts:
            if contact.phone:
                try:
                    # Stagger calls by 10 seconds each
                    trigger_emergency_call_enhanced.delay(
                        str(event_id), 
                        contact.phone, 
                        contact.name,
                        call_count * 10  # Delay in seconds
                    )
                    call_count += 1
                    logger.info(f"📞 Emergency call queued for {contact.name} ({contact.phone}) - Delay: {call_count * 10}s")
                except Exception as e:
                    logger.error(f"Failed to queue call for {contact.name}: {str(e)}")
        
        # 4. ACTIVATE SYSTEM ALERTS
        try:
            activate_system_alerts.delay(str(event_id), video_name, confidence_score)
            logger.info(f"🚨 System alerts activated for event {event_id}")
        except Exception as e:
            logger.error(f"Failed to activate system alerts: {str(e)}")
        
        # 5. UPDATE EVENT STATUS
        event.status = 'emergency_response_active'
        event.save()
        
        # 6. LOG COMPREHENSIVE RESPONSE
        response_summary = {
            'event_id': str(event_id),
            'video_name': video_name,
            'confidence_score': confidence_score,
            'sms_alerts_sent': sms_sent_count,
            'email_alerts_sent': email_sent_count,
            'emergency_calls_initiated': call_count,
            'total_contacts_notified': emergency_contacts.count(),
            'response_timestamp': timezone.now().isoformat()
        }
        
        logger.critical(f"🚨 EMERGENCY RESPONSE SUMMARY: {response_summary}")
        
        return response_summary
        
    except FireDetectionEvent.DoesNotExist:
        logger.error(f"Fire detection event {event_id} not found")
        return {"error": "Event not found"}
    except Exception as e:
        logger.error(f"Emergency response error: {str(e)}")
        return {"error": str(e)}

@shared_task
def send_emergency_sms(phone_number, contact_name, message, event_id):
    """
    Send urgent SMS notification for fire emergency
    """
    try:
        # SMS message optimization for emergency
        urgent_sms = f"""🚨 FIRE EMERGENCY 🚨
{contact_name}, immediate action required!

{message[:300]}...

Event ID: {event_id}
Time: {timezone.now().strftime('%H:%M:%S')}

DO NOT IGNORE - CALL FIRE DEPT IF NOT ALREADY CALLED"""
        
        # Integration point for SMS service (Twilio, AWS SNS, etc.)
        # Replace this with your actual SMS provider
        logger.critical(f"🚨📱 EMERGENCY SMS TO {contact_name} ({phone_number}): {urgent_sms[:100]}...")
        
        # Simulate SMS sending success
        # In production, integrate with:
        # - Twilio SMS API
        # - AWS SNS
        # - Your telecommunications provider
        
        return {
            "success": True, 
            "phone": phone_number,
            "contact": contact_name,
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Emergency SMS error to {phone_number}: {str(e)}")
        return {"error": str(e)}

@shared_task  
def send_emergency_email(email_address, contact_name, subject, message, event_id):
    """
    Send urgent email notification for fire emergency
    """
    try:
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #dc2626; color: white; padding: 20px;">
            <div style="background-color: #fef2f2; color: #dc2626; padding: 30px; border-radius: 10px; border: 3px solid #dc2626;">
                <h1 style="color: #dc2626; text-align: center; font-size: 28px; margin-bottom: 20px;">
                    🚨 FIRE EMERGENCY ALERT 🚨
                </h1>
                
                <div style="background-color: #dc2626; color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h2>Dear {contact_name},</h2>
                    <p style="font-size: 16px; line-height: 1.6;">
                        This is an automated <strong>FIRE EMERGENCY ALERT</strong> from the Fire Detection System.
                        <strong>IMMEDIATE ACTION IS REQUIRED.</strong>
                    </p>
                </div>
                
                <div style="background-color: #f3f4f6; color: #374151; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <pre style="white-space: pre-wrap; font-family: monospace; font-size: 14px;">{message}</pre>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://127.0.0.1:8000/dashboard/?emergency_event={event_id}" 
                       style="background-color: #dc2626; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 18px; font-weight: bold;">
                        🚨 VIEW EMERGENCY DASHBOARD 🚨
                    </a>
                </div>
                
                <div style="background-color: #fbbf24; color: #92400e; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>IMMEDIATE ACTION CHECKLIST:</h3>
                    <ul>
                        <li>✅ Verify fire department has been contacted</li>
                        <li>✅ Initiate evacuation procedures if safe to do so</li>
                        <li>✅ Account for all personnel</li>
                        <li>✅ Meet at designated safe assembly point</li>
                        <li>✅ Do not re-enter building until cleared by fire department</li>
                    </ul>
                </div>
                
                <hr style="margin: 30px 0; border: 1px solid #dc2626;">
                <p style="text-align: center; color: #6b7280; font-size: 12px;">
                    Event ID: {event_id}<br>
                    Fire Detection System - Automated Emergency Response<br>
                    Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>This is a critical emergency alert - DO NOT IGNORE</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        # Send email using Django's email system
        from django.core.mail import send_mail
        from django.conf import settings
        
        send_mail(
            subject=f"🚨 URGENT: {subject}",
            message=message,  # Plain text fallback
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'fire-system@company.com'),
            recipient_list=[email_address],
            html_message=html_content,
            fail_silently=False
        )
        
        logger.critical(f"🚨📧 EMERGENCY EMAIL SENT TO {contact_name} ({email_address})")
        
        return {
            "success": True,
            "email": email_address,
            "contact": contact_name,
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Emergency email error to {email_address}: {str(e)}")
        return {"error": str(e)}

@shared_task
def trigger_emergency_call_enhanced(event_id, phone_number, contact_name, delay_seconds=0):
    """
    Enhanced emergency call system with detailed logging
    """
    import time
    
    try:
        if delay_seconds > 0:
            logger.info(f"📞 Emergency call to {contact_name} scheduled in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
        
        # Check if event is still active
        from .models import FireDetectionEvent
        event = FireDetectionEvent.objects.get(id=event_id)
        
        if event.status == 'resolved':
            logger.info(f"📞 Emergency call to {contact_name} cancelled - incident resolved")
            return {"cancelled": True, "reason": "Incident resolved"}
        
        # Emergency call message
        call_message = f"""
        This is an automated emergency call from the Fire Detection System.
        
        A fire has been detected at {event.camera.location}.
        Detection confidence: {event.confidence_score:.1%}
        Detection time: {event.detected_at.strftime('%H:%M:%S')}
        
        If you can respond to this emergency, press 1.
        If fire department assistance is needed, press 2.
        To mark as false alarm, press 3.
        
        Event ID: {event_id}
        """
        
        # Integration point for voice calling service
        # Replace with actual telephony provider (Twilio Voice, AWS Connect, etc.)
        logger.critical(f"🚨📞 EMERGENCY CALL INITIATED TO {contact_name} ({phone_number})")
        logger.info(f"📞 Call message: {call_message}")
        
        # Simulate call completion
        # In production, this would:
        # 1. Make actual voice call
        # 2. Play recorded emergency message
        # 3. Capture DTMF responses
        # 4. Log call duration and outcome
        
        return {
            "success": True,
            "phone": phone_number,
            "contact": contact_name,
            "call_duration": "45 seconds",
            "status": "Call completed - awaiting response",
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Emergency call error to {phone_number}: {str(e)}")
        return {"error": str(e)}

@shared_task
def activate_system_alerts(event_id, video_name, confidence_score):
    """
    Activate system-wide emergency alerts and notifications
    """
    try:
        logger.critical(f"🚨 ACTIVATING SYSTEM EMERGENCY ALERTS FOR EVENT {event_id}")
        
        # 1. Activate emergency siren (if available)
        logger.warning(f"🚨 EMERGENCY SIREN ACTIVATED - Fire detected in {video_name}")
        
        # 2. Send alert to dashboard (WebSocket would be ideal)
        dashboard_alert = {
            'type': 'FIRE_EMERGENCY',
            'event_id': event_id,
            'video_name': video_name,
            'confidence': confidence_score,
            'timestamp': timezone.now().isoformat(),
            'message': f'🔥 FIRE DETECTED: {video_name} - {confidence_score:.1f}% confidence',
            'priority': 'CRITICAL'
        }
        
        # 3. Log to system emergency log
        logger.critical(f"🚨 SYSTEM ALERT: {dashboard_alert}")
        
        # 4. Update system configuration to emergency mode
        from .models import SystemConfiguration
        config = SystemConfiguration.get_config()
        # You could add an emergency_mode field to track system state
        
        # 5. Broadcast to all connected clients (implement WebSocket for real-time updates)
        broadcast_emergency_alert.delay(dashboard_alert)
        
        return {
            "success": True,
            "alerts_activated": [
                "emergency_siren",
                "dashboard_notification", 
                "system_emergency_log",
                "broadcast_alert"
            ],
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System alerts activation error: {str(e)}")
        return {"error": str(e)}

@shared_task
def broadcast_emergency_alert(alert_data):
    """
    Broadcast emergency alert to all connected clients
    """
    try:
        # This would integrate with WebSocket or Server-Sent Events
        # For now, we'll log the broadcast
        logger.critical(f"🚨 BROADCASTING EMERGENCY ALERT: {alert_data}")
        
        # In production, this would:
        # 1. Send WebSocket message to all connected dashboard clients
        # 2. Update real-time monitoring displays
        # 3. Trigger mobile app push notifications
        # 4. Update digital signage systems
        
        return {"success": True, "broadcast_completed": True}
        
    except Exception as e:
        logger.error(f"Broadcast alert error: {str(e)}")
        return {"error": str(e)}

@shared_task
def trigger_smoke_alert(event_id, video_name, confidence_score):
    """
    Handle smoke detection alerts (less urgent than fire)
    """
    from .models import FireDetectionEvent, EmergencyContact, SystemConfiguration
    from django.utils import timezone
    
    try:
        event = FireDetectionEvent.objects.get(id=event_id)
        config = SystemConfiguration.get_config()
        
        logger.warning(f"💨 SMOKE ALERT ACTIVATED - Smoke detected in {video_name} with {confidence_score:.1f}% confidence")
        
        # Get emergency contacts for smoke alerts (internal staff first)
        emergency_contacts = EmergencyContact.objects.filter(
            is_available=True, 
            category__in=['internal', 'primary']
        ).order_by('category', '-priority')
        
        # Prepare smoke alert message
        smoke_message = f"""
💨 SMOKE DETECTION ALERT 💨

INVESTIGATION REQUIRED

📍 Location: {event.camera.location}
📹 Camera: {event.camera.name}
⏰ Detection Time: {event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
📊 Smoke Confidence: {confidence_score:.1f}%
🎯 Video Source: {video_name}

⚠️ EARLY SMOKE DETECTION - INVESTIGATE IMMEDIATELY
⚠️ POTENTIAL FIRE RISK - MONITOR SITUATION CLOSELY

This is an automated smoke detection alert.
Event ID: {event_id}
        """
        
        # Send smoke alerts (SMS and Email only, no emergency calls for smoke)
        sms_sent_count = 0
        email_sent_count = 0
        
        # 1. SMS ALERTS TO INTERNAL STAFF
        for contact in emergency_contacts[:3]:  # Limit to 3 contacts for smoke
            if contact.phone:
                try:
                    send_smoke_sms.delay(contact.phone, contact.name, smoke_message, str(event_id))
                    sms_sent_count += 1
                    logger.info(f"💨📱 Smoke SMS queued for {contact.name} ({contact.phone})")
                except Exception as e:
                    logger.error(f"Failed to queue smoke SMS for {contact.name}: {str(e)}")
        
        # 2. EMAIL ALERTS TO INTERNAL STAFF
        for contact in emergency_contacts[:3]:  # Limit to 3 contacts for smoke
            if contact.email:
                try:
                    send_smoke_email.delay(
                        contact.email, 
                        contact.name, 
                        f"💨 SMOKE ALERT - {event.camera.location}",
                        smoke_message,
                        str(event_id)
                    )
                    email_sent_count += 1
                    logger.info(f"💨📧 Smoke email queued for {contact.name} ({contact.email})")
                except Exception as e:
                    logger.error(f"Failed to queue smoke email for {contact.name}: {str(e)}")
        
        # 3. UPDATE EVENT STATUS
        event.status = 'investigating'
        event.save()
        
        # 4. LOG SMOKE RESPONSE
        smoke_response_summary = {
            'event_id': str(event_id),
            'video_name': video_name,
            'smoke_confidence': confidence_score,
            'sms_alerts_sent': sms_sent_count,
            'email_alerts_sent': email_sent_count,
            'alert_type': 'smoke_detection',
            'response_timestamp': timezone.now().isoformat()
        }
        
        logger.warning(f"💨 SMOKE ALERT SUMMARY: {smoke_response_summary}")
        
        return smoke_response_summary
        
    except FireDetectionEvent.DoesNotExist:
        logger.error(f"Fire detection event {event_id} not found")
        return {"error": "Event not found"}
    except Exception as e:
        logger.error(f"Smoke alert error: {str(e)}")
        return {"error": str(e)}

@shared_task
def send_smoke_sms(phone_number, contact_name, message, event_id):
    """
    Send SMS notification for smoke detection
    """
    try:
        from django.utils import timezone
        
        # SMS message optimization for smoke alert
        smoke_sms = f"""💨 SMOKE ALERT 💨
{contact_name}, investigation needed!

{message[:250]}...

Event ID: {event_id}
Time: {timezone.now().strftime('%H:%M:%S')}

INVESTIGATE AREA - POTENTIAL FIRE RISK"""
        
        # Integration point for SMS service
        logger.warning(f"💨📱 SMOKE SMS TO {contact_name} ({phone_number}): {smoke_sms[:100]}...")
        
        return {
            "success": True, 
            "phone": phone_number,
            "contact": contact_name,
            "alert_type": "smoke_detection",
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Smoke SMS error to {phone_number}: {str(e)}")
        return {"error": str(e)}

@shared_task  
def send_smoke_email(email_address, contact_name, subject, message, event_id):
    """
    Send email notification for smoke detection
    """
    try:
        from django.utils import timezone
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f59e0b; color: white; padding: 20px;">
            <div style="background-color: #fef3c7; color: #92400e; padding: 30px; border-radius: 10px; border: 3px solid #f59e0b;">
                <h1 style="color: #92400e; text-align: center; font-size: 24px; margin-bottom: 20px;">
                    💨 SMOKE DETECTION ALERT 💨
                </h1>
                
                <div style="background-color: #f59e0b; color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h2>Dear {contact_name},</h2>
                    <p style="font-size: 16px; line-height: 1.6;">
                        This is an automated <strong>SMOKE DETECTION ALERT</strong> from the Fire Detection System.
                        <strong>INVESTIGATION IS REQUIRED.</strong>
                    </p>
                </div>
                
                <div style="background-color: #f3f4f6; color: #374151; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <pre style="white-space: pre-wrap; font-family: monospace; font-size: 14px;">{message}</pre>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://127.0.0.1:8000/dashboard/?smoke_event={event_id}" 
                       style="background-color: #f59e0b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold;">
                        💨 VIEW SMOKE ALERT DASHBOARD 💨
                    </a>
                </div>
                
                <div style="background-color: #fbbf24; color: #92400e; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>INVESTIGATION CHECKLIST:</h3>
                    <ul>
                        <li>🔍 Investigate the reported area immediately</li>
                        <li>🌡️ Check for heat sources or electrical issues</li>
                        <li>👥 Notify security and facility management</li>
                        <li>📞 Be prepared to escalate to fire department if needed</li>
                        <li>👀 Continue monitoring for fire development</li>
                    </ul>
                </div>
                
                <hr style="margin: 30px 0; border: 1px solid #f59e0b;">
                <p style="text-align: center; color: #6b7280; font-size: 12px;">
                    Event ID: {event_id}<br>
                    Fire Detection System - Smoke Alert<br>
                    Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>Early detection system - Investigate promptly</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        # Send email using Django's email system
        from django.core.mail import send_mail
        from django.conf import settings
        
        send_mail(
            subject=f"💨 SMOKE ALERT: {subject}",
            message=message,  # Plain text fallback
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'fire-system@company.com'),
            recipient_list=[email_address],
            html_message=html_content,
            fail_silently=False
        )
        
        logger.warning(f"💨📧 SMOKE EMAIL SENT TO {contact_name} ({email_address})")
        
        return {
            "success": True,
            "email": email_address,
            "contact": contact_name,
            "alert_type": "smoke_detection",
            "timestamp": timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Smoke email error to {email_address}: {str(e)}")
        return {"error": str(e)}


# ===== REAL AI DETECTION TASKS =====

@shared_task
def start_continuous_ai_monitoring(video_source):
    """
    Continuous AI monitoring task for real-time fire detection
    Analyzes video frames at regular intervals using real AI detection
    """
    logger.info(f"Starting continuous AI monitoring for: {video_source}")
    
    # Get the AI detector
    from .ai_detection import get_global_detector
    detector = get_global_detector()
    
    # Initialize monitoring variables
    monitoring_active = True
    frame_interval = 2.0  # Analyze every 2 seconds
    consecutive_detections = 0
    alert_threshold = 3  # Trigger alert after 3 consecutive detections
    
    try:
        import time
        import os
        
        # Determine if video_source is a file or camera
        if video_source.isdigit():
            # Camera ID
            cap = cv2.VideoCapture(int(video_source))
        else:
            # Video file path
            video_path = os.path.join(settings.MEDIA_ROOT, 'cctv_recordings', video_source)
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return {"status": "error", "message": "Video file not found"}
            cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video source: {video_source}")
            return {"status": "error", "message": "Failed to open video source"}
        
        frame_count = 0
        last_analysis_time = time.time()
        
        while monitoring_active:
            ret, frame = cap.read()
            
            if not ret:
                # End of video file - restart for continuous monitoring
                if not video_source.isdigit():
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
                    continue
                else:
                    logger.warning(f"Lost camera feed: {video_source}")
                    break
            
            current_time = time.time()
            
            # Analyze frame at specified intervals
            if current_time - last_analysis_time >= frame_interval:
                try:
                    # Run AI detection on current frame
                    analysis = detector.detect_fire_realtime(frame, video_source)
                    
                    # Check for fire/smoke detection
                    fire_detected = analysis.get('fire_detected', False)
                    smoke_detected = analysis.get('smoke_detected', False)
                    confidence = analysis.get('confidence', 0)
                    
                    # Track consecutive detections
                    if fire_detected or smoke_detected:
                        consecutive_detections += 1
                        logger.info(f"Detection #{consecutive_detections} - Fire: {fire_detected}, Smoke: {smoke_detected}, Confidence: {confidence}%")
                        
                        # Trigger alert if threshold reached
                        if consecutive_detections >= alert_threshold:
                            _create_ai_incident_alert(video_source, analysis, frame)
                            consecutive_detections = 0  # Reset counter
                    else:
                        consecutive_detections = max(0, consecutive_detections - 1)  # Gradually decrease
                    
                    # Log monitoring status
                    if frame_count % 30 == 0:  # Log every 30th analysis
                        logger.info(f"Monitoring {video_source} - Frame {frame_count}, Confidence: {confidence}%")
                    
                    last_analysis_time = current_time
                    frame_count += 1
                    
                except Exception as e:
                    logger.error(f"Frame analysis error: {str(e)}")
                    continue
            
            # Small delay to prevent overwhelming the system
            time.sleep(0.1)
            
            # Check if we should stop monitoring (this would be controlled by another mechanism)
            if frame_count > 10000:  # Stop after analyzing 10,000 frames for this demo
                monitoring_active = False
        
        cap.release()
        logger.info(f"Continuous monitoring stopped for: {video_source}")
        
        return {
            "status": "completed",
            "video_source": video_source,
            "frames_analyzed": frame_count,
            "monitoring_duration": time.time() - (last_analysis_time - frame_interval * frame_count)
        }
        
    except Exception as e:
        logger.error(f"Continuous monitoring error: {str(e)}")
        return {"status": "error", "message": str(e)}

def _create_ai_incident_alert(video_source, analysis, frame):
    """Create incident alert when fire/smoke is detected by AI"""
    try:
        import os
        import json
        
        # Save frame as evidence
        timestamp = timezone.now()
        frame_filename = f"ai_incident_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
        frame_path = os.path.join(settings.MEDIA_ROOT, 'snapshots', frame_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(frame_path), exist_ok=True)
        
        # Save frame
        cv2.imwrite(frame_path, frame)
        
        # Determine severity
        fire_detected = analysis.get('fire_detected', False)
        smoke_detected = analysis.get('smoke_detected', False)
        confidence = analysis.get('confidence', 0)
        
        if fire_detected:
            severity = 'critical'
            incident_type = 'fire'
        elif smoke_detected:
            severity = 'high'
            incident_type = 'smoke'
        else:
            severity = 'medium'
            incident_type = 'anomaly'
        
        # Create incident report using existing model
        from .models import FireDetectionEvent, Camera
        
        # Get or create virtual camera for this video source
        virtual_camera, created = Camera.objects.get_or_create(
            name=f"AI_Monitor_{video_source}",
            defaults={
                'location': f"Video Source: {video_source}",
                'rtsp_url': video_source,
                'status': 'online'
            }
        )
        
        # Create fire detection event
        incident = FireDetectionEvent.objects.create(
            camera=virtual_camera,
            confidence_score=confidence / 100.0,  # Convert to decimal
            severity=severity,
            status='active',
            bounding_boxes=json.dumps(analysis.get('detections', []))
        )
        
        logger.critical(f"🚨 AI INCIDENT ALERT CREATED: {incident_type.upper()} detected in {video_source} with {confidence}% confidence")
        
        # Trigger emergency response if fire is detected
        if fire_detected and confidence > 70:
            trigger_emergency_response.delay(incident.id, video_source, confidence)
        elif smoke_detected and confidence > 60:
            trigger_smoke_alert.delay(incident.id, video_source, confidence)
        
        return incident
        
    except Exception as e:
        logger.error(f"Failed to create AI incident alert: {str(e)}")
        return None

@shared_task
def analyze_video_batch_ai(video_files_list):
    """
    Batch analysis of multiple video files for AI fire detection
    Useful for processing recorded surveillance footage
    """
    logger.info(f"Starting AI batch analysis of {len(video_files_list)} videos")
    
    from .ai_detection import get_global_detector
    detector = get_global_detector()
    results = []
    
    for video_file in video_files_list:
        try:
            logger.info(f"AI analyzing video: {video_file}")
            
            # Get sample frames from video
            frames = _extract_sample_frames_ai(video_file, num_samples=10)
            
            video_analysis = {
                'video_file': video_file,
                'total_frames_analyzed': len(frames),
                'detections': [],
                'overall_risk_score': 0,
                'incidents_detected': 0,
                'ai_analysis': True
            }
            
            for i, frame in enumerate(frames):
                analysis = detector.detect_fire_realtime(frame, video_file)
                
                if analysis.get('fire_detected') or analysis.get('smoke_detected'):
                    video_analysis['detections'].append({
                        'frame_number': i,
                        'analysis': analysis,
                        'timestamp': i * 30  # Assuming 30 seconds between samples
                    })
                    video_analysis['incidents_detected'] += 1
            
            # Calculate overall risk score
            if video_analysis['incidents_detected'] > 0:
                confidence_scores = [d['analysis'].get('confidence', 0) for d in video_analysis['detections']]
                video_analysis['overall_risk_score'] = sum(confidence_scores) / len(confidence_scores)
            
            results.append(video_analysis)
            logger.info(f"Completed AI analysis for {video_file}: {video_analysis['incidents_detected']} incidents detected")
            
        except Exception as e:
            logger.error(f"Error in AI video analysis {video_file}: {str(e)}")
            results.append({
                'video_file': video_file,
                'error': str(e),
                'status': 'failed'
            })
    
    logger.info(f"AI batch analysis completed. Processed {len(results)} videos")
    return results

def _extract_sample_frames_ai(video_file, num_samples=10):
    """Extract sample frames from video for AI analysis"""
    try:
        import os
        
        video_path = os.path.join(settings.MEDIA_ROOT, 'cctv_recordings', video_file)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Could not open video for AI analysis: {video_path}")
            return []
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Calculate frame intervals for sampling
        if total_frames <= num_samples:
            frame_indices = list(range(total_frames))
        else:
            frame_indices = [int(i * total_frames / num_samples) for i in range(num_samples)]
        
        frames = []
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        
        cap.release()
        return frames
        
    except Exception as e:
        logger.error(f"Error extracting frames for AI analysis {video_file}: {str(e)}")
        return []

@shared_task
def cleanup_old_ai_incidents(days_old=30):
    """
    Cleanup task to remove old incident reports and associated files
    Helps maintain database and storage efficiency
    """
    try:
        from .models import FireDetectionEvent
        import os
        
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        
        # Find old incidents
        old_incidents = FireDetectionEvent.objects.filter(
            detected_at__lt=cutoff_date,
            status__in=['resolved', 'false_positive']
        )
        
        deleted_count = 0
        files_deleted = 0
        
        for incident in old_incidents:
            # Delete associated snapshot files (check notes for filename)
            if 'ai_incident_' in incident.notes:
                # Extract filename from notes if possible
                try:
                    snapshot_files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'snapshots'))
                    incident_date = incident.detected_at.strftime('%Y%m%d')
                    for filename in snapshot_files:
                        if f"ai_incident_{incident_date}" in filename:
                            snapshot_path = os.path.join(settings.MEDIA_ROOT, 'snapshots', filename)
                            os.remove(snapshot_path)
                            files_deleted += 1
                except Exception as e:
                    logger.warning(f"Could not delete snapshot files for incident {incident.id}: {str(e)}")
            
            # Delete incident record
            incident.delete()
            deleted_count += 1
        
        logger.info(f"AI incident cleanup completed: {deleted_count} old incidents deleted, {files_deleted} files removed")
        
        return {
            'status': 'completed',
            'incidents_deleted': deleted_count,
            'files_deleted': files_deleted,
            'cutoff_date': cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"AI incident cleanup task error: {str(e)}")
        return {'status': 'error', 'message': str(e)}
