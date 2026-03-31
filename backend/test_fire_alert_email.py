"""
Test Emergency Fire Alert Email
This script creates a test fire detection event and sends emergency alert emails
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
# Set email credentials
os.environ['EMAIL_HOST_USER'] = 'projectfire672@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'xskrglbrwlngaxmz'
django.setup()

from fire_detection.models import Camera, FireDetectionEvent, EmergencyContact
from fire_detection.email_service import email_service
from django.utils import timezone
import random

print("\n" + "="*60)
print("🔥 TESTING EMERGENCY FIRE ALERT EMAIL SYSTEM")
print("="*60 + "\n")

# Create or get a test camera
camera, created = Camera.objects.get_or_create(
    name="MALL_INSIDE",
    defaults={
        'location': 'Mall Interior - Food Court',
        'rtsp_url': 'file://mall_inside.mp4',
        'status': 'online'
    }
)

if created:
    print(f"✅ Created test camera: {camera.name}")
else:
    print(f"✅ Using existing camera: {camera.name}")

# Create a test fire detection event
fire_event = FireDetectionEvent.objects.create(
    camera=camera,
    confidence_score=random.uniform(0.85, 0.95),
    severity='critical',
    status='active',
    bounding_boxes='[]'
)

print(f"✅ Created fire detection event ID: {fire_event.id}")
print(f"   📍 Location: {camera.location}")
print(f"   📹 Camera: {camera.name}")
print(f"   ⏰ Time: {fire_event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   📊 Confidence: {fire_event.confidence_score * 100:.1f}%")

# Get all emergency contacts
contacts = EmergencyContact.objects.filter(is_available=True)
print(f"\n📧 Found {contacts.count()} emergency contacts:")
for contact in contacts:
    print(f"   ✅ {contact.name} - {contact.email} ({contact.category})")

print("\n" + "-"*60)
print("🚨 SENDING EMERGENCY FIRE ALERT EMAILS...")
print("-"*60 + "\n")

# Send emergency alert emails
result = email_service.send_emergency_fire_alert(fire_event)

print("\n" + "="*60)
print("📊 ALERT EMAIL RESULTS")
print("="*60)

if result['success']:
    print(f"✅ SUCCESS! Emails sent successfully")
    print(f"   📧 Emails sent: {result['sent_count']}/{result['total_recipients']}")
    
    if result.get('failed_recipients'):
        print(f"\n❌ Failed recipients:")
        for email in result['failed_recipients']:
            print(f"   ❌ {email}")

    if result['sent_count'] == result['total_recipients']:
        print(f"\n🎯 All emergency contacts have been notified!")
    else:
        print(f"\n⚠️ Partial delivery: some emergency contacts were not notified.")

    print(f"📬 Check your inbox for the emergency alert email")
    print(f"\nEmail format:")
    print(f"  🚨 EMERGENCY FIRE ALERT 🚨")
    print(f"  📍 Location: {camera.location}")
    print(f"  📹 Camera: {camera.name}")
    print(f"  ⏰ Time: {fire_event.detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  📊 Confidence: {fire_event.confidence_score * 100:.1f}%")
else:
    print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
    if result.get('failed_recipients'):
        print(f"\n❌ Failed recipients:")
        for email in result['failed_recipients']:
            print(f"   ❌ {email}")

print("\n" + "="*60)
print("✅ TEST COMPLETED")
print("="*60 + "\n")
