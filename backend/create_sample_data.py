"""
Create sample fire detection events for testing analytics charts
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

from fire_detection.models import FireDetectionEvent, Camera
from django.utils import timezone

print("🔥 Creating sample fire detection data for analytics...\n")

# Get or create sample cameras
cameras = []
camera_locations = [
    ('MALL_ENTRANCE', 'Mall Main Entrance'),
    ('MALL_INSIDE', 'Mall Interior - Food Court'),
    ('MALL_PARKING', 'Mall Parking Level 2'),
    ('MALL_ESCALATOR', 'Mall Escalator Area'),
    ('MALL_STORE', 'Mall Retail Store Area'),
]

for camera_id, location in camera_locations:
    camera, created = Camera.objects.get_or_create(
        name=camera_id,
        defaults={
            'location': location,
            'rtsp_url': f'rtsp://example.com/{camera_id.lower()}',
            'status': 'online'
        }
    )
    cameras.append(camera)
    if created:
        print(f"✅ Created camera: {camera.name} ({camera.location})")

# Create fire detection events over the last 30 days
now = timezone.now()
events_created = 0
false_alarms_created = 0

for i in range(50):  # Create 50 events
    # Random date within last 30 days
    days_ago = random.randint(0, 30)
    event_time = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    
    # Random camera
    camera = random.choice(cameras)
    
    # Random confidence score
    confidence = random.uniform(0.60, 0.98)
    
    # Determine severity based on confidence
    if confidence >= 0.90:
        severity = 'critical'
    elif confidence >= 0.80:
        severity = 'high'
    elif confidence >= 0.70:
        severity = 'medium'
    else:
        severity = 'low'
    
    # Random status (some resolved, some active, some false alarms)
    status_choice = random.choices(
        ['resolved', 'active', 'investigating', 'false_alarm'],
        weights=[60, 15, 10, 15]  # 60% resolved, 15% active, 10% investigating, 15% false alarms
    )[0]
    
    # Create the event
    event = FireDetectionEvent.objects.create(
        camera=camera,
        detection_type='fire',
        confidence_score=confidence,
        severity=severity,
        status=status_choice,
        people_count=random.randint(0, 20),
        detected_at=event_time,
        notes=f"Sample fire detection event from {camera.location}"
    )
    
    # Set resolved_at for resolved events
    if status_choice == 'resolved':
        response_time = timedelta(minutes=random.randint(2, 20))
        event.resolved_at = event_time + response_time
        event.save()
    
    events_created += 1
    if status_choice == 'false_alarm':
        false_alarms_created += 1
    
    print(f"{'✅' if status_choice != 'false_alarm' else '⚠️'} Event {i+1}: {camera.name} - {confidence*100:.1f}% confidence - {status_choice}")

print(f"\n📊 Summary:")
print(f"   Total Events Created: {events_created}")
print(f"   True Positives: {events_created - false_alarms_created}")
print(f"   False Alarms: {false_alarms_created}")
print(f"   Cameras: {len(cameras)}")
print(f"\n✅ Sample data created successfully!")
print(f"\n🌐 View analytics at: http://127.0.0.1:8000/analytics/")
