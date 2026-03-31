# Email Configuration for Fire Detection System

## SMTP Protocol Setup ✉️

The Fire Detection System uses **SMTP (Simple Mail Transfer Protocol)** for sending emergency fire alert emails.

### SMTP Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'projectfire672@gmail.com'
EMAIL_HOST_PASSWORD = 'elwtxqkajadlvsem'  # App-specific password
DEFAULT_FROM_EMAIL = 'projectfire672@gmail.com'
```

### How It Works

1. **Protocol**: SMTP (Simple Mail Transfer Protocol)
2. **Server**: Gmail SMTP Server (`smtp.gmail.com`)
3. **Port**: 587 (TLS encrypted)
4. **Security**: TLS/STARTTLS encryption enabled
5. **Authentication**: Username/Password authentication
6. **From Address**: projectfire672@gmail.com

## Emergency Contacts 🚨

The system has **9 emergency contacts** configured to receive automatic fire alerts:

### Contact List

| Name | Title | Email | Phone | Category | Priority |
|------|-------|-------|-------|----------|----------|
| Fire Department | Chief Fire Officer | padirishitha13@gmail.com | 9908339450 | fire_department | HIGH |
| Fire Department | Emergency Services | 227r1a66b3@cmrtc.ac.in | 9866406226 | fire_department | HIGH |
| Medical Emergency | Emergency Medical Services | 227r1a6675@cmrtc.ac.in | 9989647221 | medical | HIGH |
| Emergency Without Weapons | Security Response Team | padirishitha13@gmail.com | 9908339450 | security | HIGH |
| Medical Staff | Hospital Emergency Unit | 227r1a66b3@cmrtc.ac.in | 9866406226 | medical | HIGH |
| Facility Manager | Building Operations Manager | padirishitha13@gmail.com | 9908339450 | primary | HIGH |
| Security Manager | Head of Security | 227r1a6675@cmrtc.ac.in | 9989647221 | security | HIGH |
| External Services | Municipal Emergency Services | 227r1a66b3@cmrtc.ac.in | 9866406226 | external | MEDIUM |
| Nearby Police Departments | Local Police Station | padirishitha13@gmail.com | 9908339450 | external | MEDIUM |

## Email Types Sent via SMTP

### 1. Test Emails
- **Purpose**: Verify SMTP configuration
- **Subject**: `🚨 TEST: Fire Detection System Email`
- **Recipients**: All emergency contacts
- **Command**: `python test_email.py`

### 2. Fire Alert Emails
- **Purpose**: Notify about actual fire detection
- **Subject**: `[FIRE ALERT] Fire Detected - {Location}`
- **Recipients**: All active emergency contacts
- **Trigger**: Automatic when fire confidence > 80%
- **Content**: 
  - Location of fire
  - Confidence level
  - Camera name
  - Detection timestamp
  - Evacuation instructions

### 3. Emergency Response Emails
- **Purpose**: Critical fire incidents requiring immediate action
- **Subject**: `[FIRE ALERT] CRITICAL - Fire Accident Detected`
- **Recipients**: All HIGH priority contacts
- **Trigger**: Fire accident confirmed
- **Content**:
  - Fire location details
  - People in danger zone
  - Emergency procedures activated
  - Direct action required

## Testing SMTP Email System

### Test All Contacts
```bash
cd backend
python test_email.py
```

This will:
- ✅ Connect to Gmail SMTP server
- ✅ Send test emails to all 9 emergency contacts
- ✅ Verify each email delivery
- ✅ Report success/failure for each contact

### Add/Update Emergency Contacts
```bash
cd backend
python add_emergency_contacts.py
```

This will:
- 🗑️ Clear existing contacts
- ✅ Add all 9 emergency contacts from dashboard
- ✅ Configure email addresses and phone numbers
- ✅ Set priority levels
- ✅ Enable automatic alerts

## Email Notification Flow

```
Fire Detected (Confidence > 80%)
        ↓
Email Service Triggered
        ↓
SMTP Connection to Gmail (smtp.gmail.com:587)
        ↓
TLS Encryption Established
        ↓
Authentication (projectfire672@gmail.com)
        ↓
Email Sent to ALL 9 Emergency Contacts
        ↓
Delivery Confirmation Logged
        ↓
Notification Recorded in Database
```

## Email Service Features

✅ **Automatic Alerts**: Fire detection triggers automatic emails  
✅ **SMTP Protocol**: Industry-standard email delivery  
✅ **TLS Encryption**: Secure email transmission  
✅ **Multiple Recipients**: All contacts notified simultaneously  
✅ **Retry Logic**: Up to 3 retry attempts for failed deliveries  
✅ **Delivery Logging**: All emails logged in database  
✅ **HTML & Plain Text**: Both formats supported  
✅ **Priority Handling**: HIGH priority contacts notified first  

## Troubleshooting

### Email Not Sending?

1. **Check SMTP Settings**:
   ```bash
   cd backend
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.EMAIL_HOST)
   >>> print(settings.EMAIL_PORT)
   ```

2. **Test Connection**:
   ```bash
   python test_email.py
   ```

3. **Check Logs**:
   ```bash
   tail -f logs/fire_detection.log
   ```

### Common Issues

- **Authentication Failed**: Check EMAIL_HOST_PASSWORD
- **Connection Timeout**: Verify port 587 is not blocked
- **TLS Error**: Ensure EMAIL_USE_TLS = True
- **No Recipients**: Run add_emergency_contacts.py

## Security Notes

🔒 **App Password**: Using Gmail app-specific password (not regular password)  
🔒 **TLS Encryption**: All emails encrypted in transit  
🔒 **Secure Storage**: Email credentials stored in environment variables  
🔒 **Access Control**: Only authorized system can send emails  

## Email Testing Checklist

- [x] SMTP configuration verified
- [x] 9 emergency contacts added
- [x] Test emails sent successfully
- [x] All recipients receiving emails
- [x] Fire alert emails configured
- [x] Automatic triggers enabled
- [x] Delivery logging active
- [x] Error handling implemented

## Maintenance

### Update Email Credentials
Edit `.env` file or settings.py:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Add New Contact
```python
from fire_detection.models import EmergencyContact

EmergencyContact.objects.create(
    name='Contact Name',
    title='Job Title',
    email='email@example.com',
    phone='1234567890',
    category='fire_department',
    priority='high',
    is_available=True
)
```

## Support

For email system issues:
1. Check SMTP logs: `logs/fire_detection.log`
2. Test email delivery: `python test_email.py`
3. Verify contacts: Visit http://127.0.0.1:8000/emergency-contacts/

---

**Last Updated**: January 22, 2026  
**System**: Fire Detection & Emergency Response System  
**Email Protocol**: SMTP with TLS  
**Provider**: Gmail (smtp.gmail.com:587)
