import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
# Set email credentials directly
os.environ['EMAIL_HOST_USER'] = 'projectfire672@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'xskrglbrwlngaxmz'
django.setup()

from fire_detection.models import EmergencyContact
from fire_detection.email_service import email_service

# Get all emergency contacts
contacts = EmergencyContact.objects.filter(is_available=True)
print(f'\n📧 Found {contacts.count()} emergency contacts:')

for contact in contacts:
    print(f'   ✅ {contact.name} - {contact.email} ({contact.category})')

print('\n🔥 Sending TEST fire alert emails to all contacts...\n')

# Send email to ALL contacts
email_sent = 0
for contact in contacts:
    if contact.email:
        try:
            success = email_service.send_test_email(contact.email, contact.name)
            if success:
                print(f'   ✅ Email sent to {contact.name} ({contact.email})')
                email_sent += 1
            else:
                print(f'   ❌ Failed to send to {contact.name} ({contact.email})')
        except Exception as e:
            print(f'   ❌ Failed to send to {contact.name}: {e}')

print(f'\n✅ COMPLETED! Sent {email_sent} out of {contacts.count()} emails successfully!')
print('Check your email inbox to verify delivery.')
