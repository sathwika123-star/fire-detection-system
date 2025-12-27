# Management command to set up emergency contacts
from django.core.management.base import BaseCommand
from fire_detection.models import EmergencyContact

class Command(BaseCommand):
    help = 'Set up emergency contacts for fire detection system'
    
    def handle(self, *args, **options):
        # Create emergency contacts if they don't exist
        contacts = [
            {
                'name': 'Fire Department',
                'title': 'Emergency Services',
                'phone': '+1-911-FIRE-DEPT',
                'email': 'fire.dept@emergency.gov',
                'category': 'primary',
                'priority': 'high'
            },
            {
                'name': 'Medical Emergency Services',
                'title': 'Emergency Medical Team',
                'phone': '+1-911-MEDICAL',
                'email': 'medical@emergency.gov',
                'category': 'primary',
                'priority': 'high'
            },
            {
                'name': 'Building Security Chief',
                'title': 'Security Manager',
                'phone': '+1-555-SECURITY',
                'email': 'security@company.com',
                'category': 'primary',
                'priority': 'high'
            },
            {
                'name': 'Facility Manager',
                'title': 'Facilities Director',
                'phone': '+1-555-FACILITY',
                'email': 'facilities@company.com',
                'category': 'internal',
                'priority': 'medium'
            },
            {
                'name': 'Emergency Coordinator',
                'title': 'Emergency Response Coordinator',
                'phone': '+1-555-EMERGENCY',
                'email': 'emergency@company.com',
                'category': 'primary',
                'priority': 'high'
            }
        ]
        
        created_count = 0
        for contact_data in contacts:
            contact, created = EmergencyContact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created emergency contact: {contact.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Emergency contact already exists: {contact.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Emergency contacts setup complete. Created {created_count} new contacts.')
        )
