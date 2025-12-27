from django.core.management.base import BaseCommand
from fire_detection.models import EmergencyContact, SystemConfiguration

class Command(BaseCommand):
    help = 'Setup emergency contacts with updated phone numbers and emails'

    def handle(self, *args, **options):
        self.stdout.write('🚨 Setting up Emergency Contacts...')
        
        # Emergency contacts data with updated information
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
                'category': 'police',
                'priority': 'high'
            },
            {
                'name': 'Security Manager',
                'title': 'Security Chief',
                'phone': '9908339450',
                'email': 'padirishitha13@gmail.com',
                'category': 'security',
                'priority': 'medium'
            },
            {
                'name': 'Facility Manager',
                'title': 'Building Manager',
                'phone': '9989647221',
                'email': 'bellalasathwika2@gmail.com',
                'category': 'management',
                'priority': 'medium'
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for contact_data in contacts_data:
            contact, created = EmergencyContact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'✅ Created: {contact.name}')
            else:
                # Update existing contact
                for key, value in contact_data.items():
                    setattr(contact, key, value)
                contact.save()
                updated_count += 1
                self.stdout.write(f'🔄 Updated: {contact.name}')
        
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
        
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'   - Created: {created_count} contacts')
        self.stdout.write(f'   - Updated: {updated_count} contacts')
        self.stdout.write(f'   - Total contacts: {EmergencyContact.objects.count()}')
        
        self.stdout.write(f'\n🚨 Emergency Contacts:')
        for contact in EmergencyContact.objects.filter(is_available=True):
            self.stdout.write(f'   - {contact.name}: {contact.email} / {contact.phone}')
        
        self.stdout.write(f'\n🎉 Emergency contacts setup completed!')

