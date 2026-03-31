"""
Email Notification Service for Fire Detection System
Handles all email communications for emergency alerts and notifications
Uses SMTP Protocol (Gmail SMTP: smtp.gmail.com:587 with TLS)
"""

from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging
import time
import requests
from typing import List, Dict, Optional, Any, Tuple
from .models import EmergencyContact, FireDetectionEvent, AlertNotification

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """
    Service for sending email notifications to emergency contacts
    Uses SMTP Protocol for reliable email delivery
    Configured with Gmail SMTP (smtp.gmail.com:587)
    """
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'projectfire672@gmail.com')
        self.enabled = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('ENABLED', True)
        self.subject_prefix = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('SUBJECT_PREFIX', '[FIRE ALERT]')
        self.max_retries = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get('MAX_RETRIES', 3)
        self.smtp_timeout = getattr(settings, 'EMAIL_TIMEOUT', 20)
        self.email_provider = getattr(settings, 'EMERGENCY_EMAIL_SETTINGS', {}).get(
            'PROVIDER',
            getattr(settings, 'EMAIL_PROVIDER', 'smtp')
        ).lower()
        
        # SMTP Configuration
        self.smtp_host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'EMAIL_PORT', 587)
        self.smtp_user = getattr(settings, 'EMAIL_HOST_USER', 'projectfire672@gmail.com')
        self.smtp_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        self.use_tls = getattr(settings, 'EMAIL_USE_TLS', True)

        # SendGrid API Configuration
        self.sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', '')
        self.sendgrid_from_email = getattr(settings, 'SENDGRID_FROM_EMAIL', self.from_email)
        self.sendgrid_timeout = getattr(settings, 'SENDGRID_TIMEOUT', 20)
        
        logger.info(
            f"Email Service initialized with provider={self.email_provider}, SMTP={self.smtp_host}:{self.smtp_port}"
        )

    def _smtp_credentials_configured(self) -> Tuple[bool, str]:
        if not self.smtp_user or not self.smtp_password:
            return False, 'SMTP credentials are not configured (EMAIL_HOST_USER/EMAIL_HOST_PASSWORD)'
        return True, ''

    def _sendgrid_configured(self) -> Tuple[bool, str]:
        if not self.sendgrid_api_key:
            return False, 'SendGrid API key is not configured (SENDGRID_API_KEY)'
        return True, ''

    def _email_provider_configured(self) -> Tuple[bool, str]:
        if self.email_provider == 'smtp':
            return self._smtp_credentials_configured()
        if self.email_provider == 'sendgrid':
            return self._sendgrid_configured()
        if self.email_provider == 'auto':
            smtp_ok, _ = self._smtp_credentials_configured()
            sendgrid_ok, _ = self._sendgrid_configured()
            if smtp_ok or sendgrid_ok:
                return True, ''
            return False, 'Neither SMTP nor SendGrid configuration is available'
        return False, f'Unsupported email provider: {self.email_provider}'

    def _sanitize_recipients(self, recipients: List[str]) -> List[str]:
        cleaned = [recipient.strip() for recipient in recipients if recipient and recipient.strip()]
        return list(dict.fromkeys(cleaned))

    def _send_message_with_retry(self, message: EmailMessage) -> Tuple[bool, Optional[str], str]:
        smtp_modes = [('tls', self.smtp_host, self.smtp_port, self.use_tls, False)]
        if self.smtp_port != 465:
            smtp_modes.append(('ssl', self.smtp_host, 465, False, True))

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            for mode_name, host, port, use_tls, use_ssl in smtp_modes:
                connection = None
                try:
                    connection = get_connection(
                        fail_silently=False,
                        host=host,
                        port=port,
                        username=self.smtp_user,
                        password=self.smtp_password,
                        use_tls=use_tls,
                        use_ssl=use_ssl,
                        timeout=self.smtp_timeout
                    )
                    message.connection = connection
                    message.send()
                    return True, None, mode_name
                except Exception as exc:
                    last_error = str(exc)
                    logger.warning(
                        f"Email send attempt {attempt}/{self.max_retries} via {mode_name.upper()} failed: {last_error}"
                    )
                finally:
                    if connection:
                        connection.close()

            if attempt < self.max_retries:
                time.sleep(1)

        return False, last_error, 'failed'

    def _send_via_sendgrid(
        self,
        recipient: str,
        subject: str,
        plain_message: str,
        html_message: Optional[str] = None
    ) -> Tuple[bool, Optional[str], str]:
        headers = {
            'Authorization': f'Bearer {self.sendgrid_api_key}',
            'Content-Type': 'application/json'
        }

        content = [{'type': 'text/plain', 'value': plain_message}]
        if html_message:
            content.append({'type': 'text/html', 'value': html_message})

        payload = {
            'personalizations': [
                {
                    'to': [{'email': recipient}]
                }
            ],
            'from': {'email': self.sendgrid_from_email},
            'subject': subject,
            'content': content
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    'https://api.sendgrid.com/v3/mail/send',
                    headers=headers,
                    json=payload,
                    timeout=self.sendgrid_timeout
                )

                if response.status_code in (200, 202):
                    return True, None, 'sendgrid'

                response_text = (response.text or '').strip()[:500]
                last_error = f'SendGrid API error {response.status_code}: {response_text}'
                logger.warning(
                    f"Email send attempt {attempt}/{self.max_retries} via SENDGRID failed: {last_error}"
                )
            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    f"Email send attempt {attempt}/{self.max_retries} via SENDGRID failed: {last_error}"
                )

            if attempt < self.max_retries:
                time.sleep(1)

        return False, last_error, 'sendgrid'

    def _send_single_email(
        self,
        recipient: str,
        subject: str,
        plain_message: str,
        html_message: Optional[str] = None
    ) -> Tuple[bool, Optional[str], str]:
        if self.email_provider == 'sendgrid':
            return self._send_via_sendgrid(recipient, subject, plain_message, html_message)

        if self.email_provider == 'smtp':
            if html_message:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=self.from_email,
                    to=[recipient]
                )
                msg.attach_alternative(html_message, "text/html")
            else:
                msg = EmailMessage(
                    subject=subject,
                    body=plain_message,
                    from_email=self.from_email,
                    to=[recipient]
                )
            return self._send_message_with_retry(msg)

        if self.email_provider == 'auto':
            smtp_ok, _ = self._smtp_credentials_configured()
            if smtp_ok:
                if html_message:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=self.from_email,
                        to=[recipient]
                    )
                    msg.attach_alternative(html_message, "text/html")
                else:
                    msg = EmailMessage(
                        subject=subject,
                        body=plain_message,
                        from_email=self.from_email,
                        to=[recipient]
                    )

                sent, error_message, mode = self._send_message_with_retry(msg)
                if sent:
                    return sent, error_message, mode

                sendgrid_ok, _ = self._sendgrid_configured()
                if sendgrid_ok:
                    return self._send_via_sendgrid(recipient, subject, plain_message, html_message)
                return False, error_message, mode

            sendgrid_ok, sendgrid_message = self._sendgrid_configured()
            if sendgrid_ok:
                return self._send_via_sendgrid(recipient, subject, plain_message, html_message)
            return False, sendgrid_message, 'auto'

        return False, f'Unsupported email provider: {self.email_provider}', self.email_provider
    
    def send_emergency_fire_alert(
        self, 
        incident: FireDetectionEvent, 
        recipients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
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

            creds_ok, creds_message = self._email_provider_configured()
            if not creds_ok:
                logger.error(creds_message)
                return {'success': False, 'message': creds_message}
            
            # Get recipients if not provided
            if not recipients:
                contacts = EmergencyContact.objects.filter(
                    is_available=True
                ).exclude(email__isnull=True).exclude(email='')
                recipients = [contact.email for contact in contacts]

            recipients = self._sanitize_recipients(recipients)
            
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
            last_error = None
            
            for recipient in recipients:
                try:
                    sent, error_message, transport_mode = self._send_single_email(
                        recipient=recipient,
                        subject=subject,
                        plain_message=message,
                        html_message=html_message
                    )
                    if not sent:
                        raise RuntimeError(error_message or 'Email send failed')

                    sent_count += 1
                    
                    # Log notification in database
                    self._log_notification(
                        incident,
                        recipient,
                        'email',
                        'sent',
                        subject=subject,
                        message=message
                    )
                    
                    logger.info(f"Emergency alert sent to {recipient} via {transport_mode.upper()}")
                    
                except Exception as e:
                    last_error = str(e)
                    logger.error(f"Failed to send email to {recipient}: {last_error}")
                    failed_recipients.append(recipient)
                    self._log_notification(
                        incident,
                        recipient,
                        'email',
                        'failed',
                        subject=subject,
                        message=message,
                        error_message=last_error
                    )

            success = sent_count > 0
            if success:
                status_message = f'Sent {sent_count} of {len(recipients)} emergency alert emails'
            else:
                status_message = f'Failed to send emergency alert emails to all recipients: {last_error or "Unknown SMTP error"}'
            
            return {
                'success': success,
                'sent_count': sent_count,
                'total_recipients': len(recipients),
                'failed_recipients': failed_recipients,
                'message': status_message
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
            creds_ok, creds_message = self._email_provider_configured()
            if not creds_ok:
                logger.error(creds_message)
                return False

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

            sent, error_message, transport_mode = self._send_single_email(
                recipient=recipient,
                subject=subject,
                plain_message=message,
                html_message=None
            )
            if not sent:
                raise RuntimeError(error_message or 'Email send failed')
            
            logger.info(f"Test email sent successfully to {recipient} via {transport_mode.upper()}")
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
            creds_ok, creds_message = self._email_provider_configured()
            if not creds_ok:
                logger.error(creds_message)
                return False

            sent, error_message, transport_mode = self._send_single_email(
                recipient=to_email,
                subject=subject,
                plain_message=message,
                html_message=None
            )
            if not sent:
                raise RuntimeError(error_message or 'Email send failed')
            
            logger.info(f"Email sent successfully to {to_email} via {transport_mode.upper()}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_incident_resolution_email(
        self, 
        incident: FireDetectionEvent, 
        resolution_notes: str,
        recipients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
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
            creds_ok, creds_message = self._email_provider_configured()
            if not creds_ok:
                logger.error(creds_message)
                return {'success': False, 'message': creds_message}

            if not recipients:
                contacts = EmergencyContact.objects.filter(
                    is_available=True
                ).exclude(email__isnull=True).exclude(email='')
                recipients = [contact.email for contact in contacts]

            recipients = self._sanitize_recipients(recipients)
            
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
            failed_recipients = []
            for recipient in recipients:
                try:
                    sent, error_message, _ = self._send_single_email(
                        recipient=recipient,
                        subject=subject,
                        plain_message=message,
                        html_message=None
                    )
                    if not sent:
                        raise RuntimeError(error_message or 'Email send failed')

                    sent_count += 1
                except Exception as e:
                    logger.error(f"Failed to send resolution email to {recipient}: {str(e)}")
                    failed_recipients.append(recipient)

            success = sent_count > 0
            
            return {
                'success': success,
                'sent_count': sent_count,
                'total_recipients': len(recipients),
                'failed_recipients': failed_recipients,
                'message': f'Sent {sent_count} of {len(recipients)} resolution emails'
            }
            
        except Exception as e:
            logger.error(f"Error sending resolution emails: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_bulk_alert(
        self, 
        subject: str, 
        message: str, 
        category: Optional[str] = None
    ) -> Dict[str, Any]:
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
            creds_ok, creds_message = self._email_provider_configured()
            if not creds_ok:
                logger.error(creds_message)
                return {'success': False, 'message': creds_message}

            # Get contacts
            contacts_query = EmergencyContact.objects.filter(is_available=True)
            if category:
                contacts_query = contacts_query.filter(category=category)
            
            contacts = contacts_query.exclude(email__isnull=True).exclude(email='')
            recipients = self._sanitize_recipients([contact.email for contact in contacts])
            
            if not recipients:
                return {'success': False, 'message': 'No recipients available'}
            
            full_subject = f"{self.subject_prefix} {subject}"
            
            sent_count = 0
            failed_recipients = []
            for recipient in recipients:
                try:
                    sent, error_message, _ = self._send_single_email(
                        recipient=recipient,
                        subject=full_subject,
                        plain_message=message,
                        html_message=None
                    )
                    if not sent:
                        raise RuntimeError(error_message or 'Email send failed')

                    sent_count += 1
                except Exception as e:
                    logger.error(f"Failed to send bulk alert to {recipient}: {str(e)}")
                    failed_recipients.append(recipient)

            success = sent_count > 0
            
            return {
                'success': success,
                'sent_count': sent_count,
                'total_recipients': len(recipients),
                'failed_recipients': failed_recipients,
                'message': f'Sent {sent_count} of {len(recipients)} bulk alert emails'
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
        subject: str = '',
        message: str = '',
        error_message: str = None
    ):
        """Log notification attempt to database"""
        try:
            message_body = message or ''
            if error_message:
                message_body = f"Delivery failed: {error_message}\n\n{message_body}".strip()

            AlertNotification.objects.create(
                fire_event=incident,
                notification_type=notification_type,
                recipient_contact=recipient,
                message_title=subject or f"{self.subject_prefix} Notification",
                message_body=message_body,
                status=status,
                urgency_level='critical' if getattr(incident, 'severity', '') in ('high', 'critical') else 'high',
                sent_at=timezone.now() if status in ('sent', 'delivered') else None
            )
        except Exception as e:
            logger.error(f"Failed to log notification: {str(e)}")


# Create singleton instance
email_service = EmailNotificationService()
