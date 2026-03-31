#!/usr/bin/env python
"""
Setup Emergency Contacts for Fire Detection System
This script creates emergency contacts that will receive automatic notifications
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

from fire_detection.models import EmergencyContact, SystemConfiguration
from django.utils import timezone

def setup_emergency_contacts():
    """Create emergency contacts for automatic notifications"""
    
    print("🚨 Setting up Emergency Contacts for Fire Detection System...")
    
    # Emergency contacts data - Updated with actual contact information
    contacts_data = [
        {
            'name': 'Fire Department',
            'title': 'Emergency Services',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'fire_department',
            'priority': 'high'
        },
        {
            'name': 'Emergency Medical Services',
            'title': 'Paramedics',
            'phone': '9989647221',
            'email': 'bellalasathwika2@gmail.com',
            'category': 'medical',
            'priority': 'high'
        },
        {
            'name': 'Metro Police Department',
            'title': 'Law Enforcement',
            'phone': '9866406226',
            'email': 'muppidojuspoorthi921@gmail.com',
            'category': 'external',
            'priority': 'high'
        },
        {
            'name': 'Security Manager',
            'title': 'Security Chief',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'primary',
            'priority': 'high'
        },
        {
            'name': 'Facility Manager',
            'title': 'Building Manager',
            'phone': '9989647221',
            'email': 'bellalasathwika2@gmail.com',
            'category': 'primary',
            'priority': 'high'
        }
    ]
    
    # Create or update emergency contacts
    created_count = 0
    updated_count = 0
    
    for contact_data in contacts_data:
        contact, created = EmergencyContact.objects.get_or_create(
            name=contact_data['name'],
            defaults=contact_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Created emergency contact: {contact.name}")
        else:
            # Update existing contact
            for key, value in contact_data.items():
                setattr(contact, key, value)
            contact.save()
            updated_count += 1
            print(f"🔄 Updated emergency contact: {contact.name}")
    
    # Setup system configuration
    config, created = SystemConfiguration.objects.get_or_create(
        pk=1,
        defaults={
            'detection_threshold': 0.5,
            'auto_alert_threshold': 0.8,
            'alert_cooldown_minutes': 5,
            'auto_emergency_call': True,
            'emergency_call_delay_seconds': 30,
            'detection_confidence_threshold': 0.7,
            'sms_notifications': True,
            'email_notifications': True,
            'siren_activation': True
        }
    )
    
    if created:
        print("✅ Created system configuration")
    else:
        print("🔄 System configuration already exists")
    
    print(f"\n📊 Summary:")
    print(f"   - Created: {created_count} contacts")
    print(f"   - Updated: {updated_count} contacts")
    print(f"   - Total contacts: {EmergencyContact.objects.count()}")
    print(f"   - System configuration: {'✅ Active' if config.email_notifications else '❌ Inactive'}")
    
    print(f"\n🚨 Emergency Contacts Ready:")
    for contact in EmergencyContact.objects.filter(is_available=True):
        print(f"   - {contact.name} ({contact.category}) - {contact.email} / {contact.phone}")
    
    print(f"\n🔥 Automatic Fire Detection System is now configured!")
    print(f"   - Email notifications: {'✅ Enabled' if config.email_notifications else '❌ Disabled'}")
    print(f"   - Phone calls: {'✅ Enabled' if config.auto_emergency_call else '❌ Disabled'}")
    print(f"   - Confidence threshold: {config.detection_confidence_threshold * 100:.0f}%")
    
    return True

if __name__ == "__main__":
    try:
        setup_emergency_contacts()
        print("\n🎉 Emergency contacts setup completed successfully!")
    except Exception as e:
        print(f"\n❌ Error setting up emergency contacts: {str(e)}")
        sys.exit(1)
