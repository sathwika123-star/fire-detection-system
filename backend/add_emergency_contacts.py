#!/usr/bin/env python
"""
Add Emergency Contacts from Dashboard
This script adds the emergency contacts shown in the dashboard
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

from fire_detection.models import EmergencyContact
from django.utils import timezone

def add_emergency_contacts():
    """Add emergency contacts from the dashboard screenshot"""
    
    print("🚨 Adding Emergency Contacts to Fire Detection System...")
    
    # Emergency contacts data from the dashboard
    contacts_data = [
        # Primary Emergency Contacts
        {
            'name': 'Fire Department',
            'title': 'Chief Fire Officer',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'fire_department',
            'priority': 'high',
            'is_available': True
        },
        {
            'name': 'Fire Department',
            'title': 'Emergency Services',
            'phone': '9866406226',
            'email': '227r1a66b3@cmrtc.ac.in',
            'category': 'fire_department',
            'priority': 'high',
            'is_available': True
        },
        
        # Medical Emergency
        {
            'name': 'Medical Emergency',
            'title': 'Emergency Medical Services',
            'phone': '9989647221',
            'email': '227r1a6675@cmrtc.ac.in',
            'category': 'medical',
            'priority': 'high',
            'is_available': True
        },
        
        # Emergency Without Weapons
        {
            'name': 'Emergency Without Weapons',
            'title': 'Security Response Team',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'security',
            'priority': 'high',
            'is_available': True
        },
        
        # Medical Staff
        {
            'name': 'Medical Staff',
            'title': 'Hospital Emergency Unit',
            'phone': '9866406226',
            'email': '227r1a66b3@cmrtc.ac.in',
            'category': 'medical',
            'priority': 'high',
            'is_available': True
        },
        
        # Facility Manager
        {
            'name': 'Facility Manager',
            'title': 'Building Operations Manager',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'primary',
            'priority': 'high',
            'is_available': True
        },
        
        # Security Manager
        {
            'name': 'Security Manager',
            'title': 'Head of Security',
            'phone': '9989647221',
            'email': '227r1a6675@cmrtc.ac.in',
            'category': 'security',
            'priority': 'high',
            'is_available': True
        },
        
        # External Services
        {
            'name': 'External Services',
            'title': 'Municipal Emergency Services',
            'phone': '9866406226',
            'email': '227r1a66b3@cmrtc.ac.in',
            'category': 'external',
            'priority': 'medium',
            'is_available': True
        },
        
        # Nearby Police Departments
        {
            'name': 'Nearby Police Departments',
            'title': 'Local Police Station',
            'phone': '9908339450',
            'email': 'padirishitha13@gmail.com',
            'category': 'external',
            'priority': 'medium',
            'is_available': True
        },
    ]
    
    # Clear existing contacts first
    print("🗑️  Clearing existing contacts...")
    EmergencyContact.objects.all().delete()
    
    # Create emergency contacts
    created_count = 0
    
    for contact_data in contacts_data:
        contact = EmergencyContact.objects.create(**contact_data)
        created_count += 1
        print(f"✅ Created: {contact.name} - {contact.title}")
        print(f"   📧 Email: {contact.email}")
        print(f"   📞 Phone: {contact.phone}")
        print(f"   🏷️  Category: {contact.category}")
        print()
    
    print(f"\n📊 Summary:")
    print(f"   - Created: {created_count} contacts")
    print(f"   - Total active contacts: {EmergencyContact.objects.filter(is_available=True).count()}")
    
    print(f"\n🚨 Emergency Contacts Active:")
    for contact in EmergencyContact.objects.filter(is_available=True):
        print(f"   ✅ {contact.name} ({contact.category})")
        print(f"      📧 {contact.email} | 📞 {contact.phone}")
    
    print(f"\n🔥 Fire Detection System Emergency Response is configured!")
    print(f"   📧 SMTP Email: Enabled (Gmail SMTP)")
    print(f"   🚨 Auto-alerts: Active")
    print(f"   📬 All contacts will receive fire alerts via email")
    
    return True

if __name__ == "__main__":
    try:
        add_emergency_contacts()
        print("\n🎉 Emergency contacts added successfully!")
        print("✉️  Test the email system by running: python test_email.py")
    except Exception as e:
        print(f"\n❌ Error adding emergency contacts: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
