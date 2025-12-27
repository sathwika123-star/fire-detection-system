#!/usr/bin/env python3
"""
Create Django Superuser for Fire Detection System
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create a superuser for Django admin"""
    
    username = 'admin'
    email = 'admin@firedetection.com'
    password = 'firedetection123'
    
    if User.objects.filter(username=username).exists():
        print(f"⚠️ Superuser '{username}' already exists")
        return
    
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser created:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   URL: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    create_superuser()
