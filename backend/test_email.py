import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

from fire_detection.models import EmergencyContact
from django.core.mail import send_mail

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
            send_mail(
                subject='🚨 TEST: Fire Detection System Email',
                message=f'Hello {contact.name}, This is a TEST email from the Fire Detection System to verify automatic email delivery to all emergency contacts.',
                from_email='projectfire672@gmail.com',
                recipient_list=[contact.email],
                fail_silently=False
            )
            print(f'   ✅ Email sent to {contact.name} ({contact.email})')
            email_sent += 1
        except Exception as e:
            print(f'   ❌ Failed to send to {contact.name}: {e}')

print(f'\n✅ COMPLETED! Sent {email_sent} out of {contacts.count()} emails successfully!')
print('Check your email inbox to verify delivery.')
