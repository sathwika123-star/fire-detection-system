"""
Email Notification Service for Fire Detection System
Handles all email communications for emergency alerts and notifications
"""

from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging
from typing import List, Dict, Optional
from .models import EmergencyContact, FireDetectionEvent, AlertNotification

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for sending email notifications to emergency contacts"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'padirishitha13@gmail.com')
        self.enabled = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('ENABLED', True)
        self.subject_prefix = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('SUBJECT_PREFIX', '[FIRE ALERT]')
        self.max_retries = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('MAX_RETRIES', 3)
    
    def send_emergency_fire_alert(
        self, 
        incident: FireDetectionEvent, 
        recipients: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Send emergency fire alert to specified recipients or all active emergency contacts
        
        Args:
            incident: FireDetectionEvent instance
            recipients: Optional list of email addresses. If None, sends to all active contacts
            
        Returns:
            Dictionary with success status and details
        """
        try:
            if not self.enabled:
                logger.info("Email notifications are disabled")
                return {'success': False, 'message': 'Email notifications disabled'}
            
            # Get recipients if not provided
            if not recipients:
                contacts = EmergencyContact.objects.filter(
                    is_available=True
                ).exclude(email__isnull=True).exclude(email='')
                recipients = [contact.email for contact in contacts]
            
            if not recipients:
                logger.warning("No recipients found for emergency alert")
                return {'success': False, 'message': 'No recipients available'}
            
            # Prepare email content
            subject = f"{self.subject_prefix} Fire Detected - {incident.camera.location}"
            
            # Create plain text message
            message = self._create_plain_text_alert(incident)
            
            # Create HTML message
            html_message = self._create_html_alert(incident)
            
            # Send email
            sent_count = 0
            failed_recipients = []
            
            for recipient in recipients:
                try:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=message,
                        from_email=self.from_email,
                        to=[recipient]
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send()
                    sent_count += 1
                    
                    # Log notification in database
                    self._log_notification(incident, recipient, 'email', 'sent')
                    
                    logger.info(f"Emergency alert sent to {recipient}")
                    
                except Exception as e:
                    logger.error(f"Failed to send email to {recipient}: {str(e)}")
                    failed_recipients.append(recipient)
                    self._log_notification(incident, recipient, 'email', 'failed', str(e))
            
            return {
                'success': True,
                'sent_count': sent_count,
                'total_recipients': len(recipients),
                'failed_recipients': failed_recipients
            }
            
        except Exception as e:
            logger.error(f"Error sending emergency alerts: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_test_email(self, recipient: str, contact_name: str) -> bool:
        """
        Send a test email to verify contact information
        
        Args:
            recipient: Email address to send test to
            contact_name: Name of the contact
            
        Returns:
            Boolean indicating success
        """
        try:
            subject = f"{self.subject_prefix} Test Notification"
            message = f"""
Hello {contact_name},

This is a test email from the Fire Detection System.

If you receive this message, your email contact information is correctly configured 
and you will receive emergency alerts when needed.

System Information:
- Timestamp: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
- System Status: Active
- Email Service: Operational

Please keep this contact information up to date.

Best regards,
Fire Detection System
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[recipient],
                fail_silently=False
            )
            
            logger.info(f"Test email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test email to {recipient}: {str(e)}")
            return False
    
    def send_email(self, to_email: str, subject: str, message: str, recipient_name: str = None) -> bool:
        """
        Generic method to send email to any recipient
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Email message body
            recipient_name: Optional recipient name
            
        Returns:
            Boolean indicating success
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[to_email],
                fail_silently=False
            )
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_incident_resolution_email(
        self, 
        incident: FireDetectionEvent, 
        resolution_notes: str,
        recipients: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Send email notification when an incident is resolved
        
        Args:
            incident: FireDetectionEvent instance
            resolution_notes: Notes about the resolution
            recipients: Optional list of email addresses
            
        Returns:
            Dictionary with success status and details
        """
        try:
            if not recipients:
                contacts = EmergencyContact.objects.filter(
                    is_available=True
                ).exclude(email__isnull=True).exclude(email='')
                recipients = [contact.email for contact in contacts]
            
            if not recipients:
                return {'success': False, 'message': 'No recipients available'}
            
            subject = f"{self.subject_prefix} Incident Resolved - {incident.camera.location}"
            
            message = f"""
INCIDENT RESOLVED

Location: {incident.camera.location}
Camera: {incident.camera.name}
Detected At: {incident.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
Resolved At: {incident.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if incident.resolved_at else 'N/A'}
Confidence: {incident.confidence_score}%

Resolution Notes:
{resolution_notes}

The situation has been addressed and the area is now safe.

Fire Detection System
"""
            
            sent_count = 0
            for recipient in recipients:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=self.from_email,
                        recipient_list=[recipient],
                        fail_silently=False
                    )
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Failed to send resolution email to {recipient}: {str(e)}")
            
            return {
                'success': True,
                'sent_count': sent_count,
                'total_recipients': len(recipients)
            }
            
        except Exception as e:
            logger.error(f"Error sending resolution emails: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_bulk_alert(
        self, 
        subject: str, 
        message: str, 
        category: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send bulk alert to all or specific category of emergency contacts
        
        Args:
            subject: Email subject
            message: Email message body
            category: Optional filter by contact category
            
        Returns:
            Dictionary with success status and details
        """
        try:
            # Get contacts
            contacts_query = EmergencyContact.objects.filter(is_available=True)
            if category:
                contacts_query = contacts_query.filter(category=category)
            
            contacts = contacts_query.exclude(email__isnull=True).exclude(email='')
            recipients = [contact.email for contact in contacts]
            
            if not recipients:
                return {'success': False, 'message': 'No recipients available'}
            
            full_subject = f"{self.subject_prefix} {subject}"
            
            sent_count = 0
            for recipient in recipients:
                try:
                    send_mail(
                        subject=full_subject,
                        message=message,
                        from_email=self.from_email,
                        recipient_list=[recipient],
                        fail_silently=False
                    )
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Failed to send bulk alert to {recipient}: {str(e)}")
            
            return {
                'success': True,
                'sent_count': sent_count,
                'total_recipients': len(recipients)
            }
            
        except Exception as e:
            logger.error(f"Error sending bulk alerts: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _create_plain_text_alert(self, incident: FireDetectionEvent) -> str:
        """Create plain text emergency alert message"""
        return f"""
🚨 EMERGENCY FIRE ALERT 🚨

FIRE DETECTED - IMMEDIATE ACTION REQUIRED

Location: {incident.camera.location}
Camera: {incident.camera.name}
Detection Time: {incident.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
Confidence Level: {incident.confidence_score}%
Severity: {incident.severity.upper() if hasattr(incident, 'severity') else 'HIGH'}

IMMEDIATE ACTIONS REQUIRED:
1. Evacuate the area immediately
2. Alert building occupants
3. Call emergency services: 911
4. Activate fire suppression systems
5. Ensure all personnel are accounted for

System Status: ALERT ACTIVE
Alert ID: {incident.id}

This is an automated alert from the Fire Detection System.
Respond immediately as per emergency protocols.

For system status: http://127.0.0.1:8000/dashboard/
Emergency contacts: http://127.0.0.1:8000/emergency-contacts/

Fire Detection System
Automated Alert - Do Not Reply
"""
    
    def _create_html_alert(self, incident: FireDetectionEvent) -> str:
        """Create HTML formatted emergency alert message"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #1a1a1a; color: #ffffff; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #2d2d2d; border-radius: 10px; overflow: hidden; }}
        .header {{ background-color: #dc2626; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; color: #ffffff; font-size: 24px; }}
        .content {{ padding: 30px; }}
        .alert-box {{ background-color: #991b1b; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }}
        .info-item {{ background-color: #1a1a1a; padding: 15px; border-radius: 5px; }}
        .info-label {{ color: #9ca3af; font-size: 12px; margin-bottom: 5px; }}
        .info-value {{ color: #ffffff; font-size: 16px; font-weight: bold; }}
        .actions {{ background-color: #1a1a1a; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .actions h3 {{ color: #dc2626; margin-top: 0; }}
        .actions ol {{ padding-left: 20px; }}
        .actions li {{ margin: 10px 0; }}
        .footer {{ background-color: #1a1a1a; padding: 20px; text-align: center; color: #9ca3af; font-size: 12px; }}
        .button {{ display: inline-block; background-color: #dc2626; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 EMERGENCY FIRE ALERT 🚨</h1>
        </div>
        
        <div class="content">
            <div class="alert-box">
                <h2 style="margin-top: 0; color: #ffffff;">FIRE DETECTED - IMMEDIATE ACTION REQUIRED</h2>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Location</div>
                    <div class="info-value">{incident.camera.location}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Camera</div>
                    <div class="info-value">{incident.camera.name}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Detection Time</div>
                    <div class="info-value">{incident.detected_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Confidence Level</div>
                    <div class="info-value">{incident.confidence_score}%</div>
                </div>
            </div>
            
            <div class="actions">
                <h3>IMMEDIATE ACTIONS REQUIRED:</h3>
                <ol>
                    <li>Evacuate the area immediately</li>
                    <li>Alert building occupants</li>
                    <li>Call emergency services: 911</li>
                    <li>Activate fire suppression systems</li>
                    <li>Ensure all personnel are accounted for</li>
                </ol>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/dashboard/" class="button">View Dashboard</a>
                <a href="http://127.0.0.1:8000/emergency-contacts/" class="button">Emergency Contacts</a>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background-color: #1a1a1a; border-radius: 5px;">
                <strong>Alert ID:</strong> {incident.id}<br>
                <strong>System Status:</strong> ALERT ACTIVE
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated alert from the Fire Detection System.</p>
            <p>Respond immediately as per emergency protocols.</p>
            <p>Automated Alert - Do Not Reply</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _log_notification(
        self, 
        incident: FireDetectionEvent, 
        recipient: str, 
        notification_type: str, 
        status: str,
        error_message: str = None
    ):
        """Log notification attempt to database"""
        try:
            # Get or create the contact
            contact = EmergencyContact.objects.filter(email=recipient).first()
            
            AlertNotification.objects.create(
                fire_event=incident,
                emergency_contact=contact,
                notification_type=notification_type,
                status=status,
                error_message=error_message
            )
        except Exception as e:
            logger.error(f"Failed to log notification: {str(e)}")


# Create singleton instance
email_service = EmailNotificationService()
