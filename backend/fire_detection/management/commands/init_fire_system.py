# Django Management Command - Initialize Fire Detection System
from django.core.management.base import BaseCommand
from django.utils import timezone
from fire_detection.models import Camera, EmergencyContact, SystemConfiguration
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Django management command to initialize the fire detection system
    with sample data and default configuration.
    
    Usage: python manage.py init_fire_system
    """
    
    help = 'Initialize Fire Detection System with sample data and default configuration'
    
    def add_arguments(self, parser):
        """Add command line arguments"""
        parser.add_argument(
            '--skip-cameras',
            action='store_true',
            help='Skip creating sample cameras',
        )
        parser.add_argument(
            '--skip-contacts',
            action='store_true', 
            help='Skip creating sample emergency contacts',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force initialization even if data exists',
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('Initializing Fire Detection System...')
        )
        
        try:
            # Initialize system configuration
            self.init_system_config(options['force'])
            
            # Initialize cameras if not skipped
            if not options['skip_cameras']:
                self.init_cameras(options['force'])
            
            # Initialize emergency contacts if not skipped
            if not options['skip_contacts']:
                self.init_emergency_contacts(options['force'])
            
            self.stdout.write(
                self.style.SUCCESS('Fire Detection System initialized successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Initialization failed: {str(e)}')
            )
            logger.error(f'Fire system initialization error: {str(e)}')
    
    def init_system_config(self, force=False):
        """Initialize system configuration"""
        if SystemConfiguration.objects.exists() and not force:
            self.stdout.write(
                self.style.WARNING('System configuration already exists. Use --force to override.')
            )
            return
        
        # Create or update system configuration
        config, created = SystemConfiguration.objects.get_or_create(
            defaults={
                'detection_confidence_threshold': 0.7,
                'alert_cooldown_minutes': 5,
                'auto_emergency_call': False,
                'emergency_call_delay_seconds': 30,
                'sms_notifications_enabled': True,
                'email_notifications_enabled': True,
                'notification_sound_enabled': True,
                'fire_department_number': '911',
                'system_admin_email': 'admin@firedetection.com',
                'max_false_alarms_per_day': 10,
                'system_maintenance_mode': False,
                'detection_areas': [
                    {
                        'name': 'Main Building',
                        'cameras': [],
                        'priority': 'high'
                    }
                ]
            }
        )
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(f'{action} system configuration')
        )
    
    def init_cameras(self, force=False):
        """Initialize sample cameras"""
        if Camera.objects.exists() and not force:
            self.stdout.write(
                self.style.WARNING('Cameras already exist. Use --force to override.')
            )
            return
        
        sample_cameras = [
            {
                'name': 'Main Entrance Camera',
                'location': 'Building Main Entrance',
                'ip_address': '192.168.1.101',
                'port': 554,
                'username': 'admin',
                'password': 'admin123',
                'rtsp_url': 'rtsp://192.168.1.101:554/stream1',
                'status': 'online',
                'is_recording': True,
                'is_detection_enabled': True,
                'detection_sensitivity': 0.7
            },
            {
                'name': 'Parking Lot Camera',
                'location': 'Employee Parking Lot',
                'ip_address': '192.168.1.102',
                'port': 554,
                'username': 'admin',
                'password': 'admin123',
                'rtsp_url': 'rtsp://192.168.1.102:554/stream1',
                'status': 'online',
                'is_recording': True,
                'is_detection_enabled': True,
                'detection_sensitivity': 0.6
            },
            {
                'name': 'Warehouse Camera 1',
                'location': 'Warehouse Section A',
                'ip_address': '192.168.1.103',
                'port': 554,
                'username': 'admin',
                'password': 'admin123',
                'rtsp_url': 'rtsp://192.168.1.103:554/stream1',
                'status': 'online',
                'is_recording': True,
                'is_detection_enabled': True,
                'detection_sensitivity': 0.8
            },
            {
                'name': 'Office Area Camera',
                'location': 'Office Floor 2',
                'ip_address': '192.168.1.104',
                'port': 554,
                'username': 'admin',
                'password': 'admin123',
                'rtsp_url': 'rtsp://192.168.1.104:554/stream1',
                'status': 'maintenance',
                'is_recording': False,
                'is_detection_enabled': False,
                'detection_sensitivity': 0.7
            }
        ]
        
        created_count = 0
        for camera_data in sample_cameras:
            camera, created = Camera.objects.get_or_create(
                name=camera_data['name'],
                defaults=camera_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} sample cameras')
        )
    
    def init_emergency_contacts(self, force=False):
        """Initialize sample emergency contacts"""
        if EmergencyContact.objects.exists() and not force:
            self.stdout.write(
                self.style.WARNING('Emergency contacts already exist. Use --force to override.')
            )
            return
        
        sample_contacts = [
            {
                'name': 'City Fire Department',
                'phone': '+1-555-FIRE-911',
                'email': 'dispatch@cityfire.gov',
                'category': 'fire_department',
                'priority': 1,
                'is_available': True,
                'notes': 'Primary emergency response for fire incidents'
            },
            {
                'name': 'Police Emergency Dispatch',
                'phone': '+1-555-POLICE-1',
                'email': 'dispatch@citypolice.gov',
                'category': 'police',
                'priority': 2,
                'is_available': True,
                'notes': 'Secondary emergency response'
            },
            {
                'name': 'Emergency Medical Services',
                'phone': '+1-555-EMS-HELP',
                'email': 'dispatch@cityems.gov',
                'category': 'medical',
                'priority': 2,
                'is_available': True,
                'notes': 'Medical emergency response'
            },
            {
                'name': 'Building Security Manager',
                'phone': '+1-555-SECURITY',
                'email': 'security@company.com',
                'category': 'security',
                'priority': 3,
                'is_available': True,
                'notes': 'On-site security coordination'
            },
            {
                'name': 'Facility Manager',
                'phone': '+1-555-FACILITY',
                'email': 'facilities@company.com',
                'category': 'management',
                'priority': 3,
                'is_available': True,
                'notes': 'Building systems and evacuation procedures'
            },
            {
                'name': 'IT System Administrator',
                'phone': '+1-555-IT-ADMIN',
                'email': 'admin@company.com',
                'category': 'management',
                'priority': 4,
                'is_available': True,
                'notes': 'Fire detection system technical support'
            }
        ]
        
        created_count = 0
        for contact_data in sample_contacts:
            contact, created = EmergencyContact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} emergency contacts')
        )
    
    def handle_database_error(self, error):
        """Handle database-related errors"""
        self.stdout.write(
            self.style.ERROR(f'Database error: {str(error)}')
        )
        self.stdout.write(
            self.style.WARNING('Make sure to run migrations first: python manage.py migrate')
        )
