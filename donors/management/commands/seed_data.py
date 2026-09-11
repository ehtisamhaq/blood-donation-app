from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from donors.models import DonorProfile, BloodRequest, BloodGroup, UrgencyLevel
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with realistic sample donors and emergency blood requests'

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample donors and emergency requests...")

        sample_donors_data = [
            {"username": "sarah_j", "first_name": "Sarah", "last_name": "Jenkins", "email": "sarah.j@example.com", "blood_group": "O-", "phone": "+1 555-0192", "city": "New York", "total": 5, "days_ago": 120, "bio": "Universal donor O-. Happy to help in any urgent surgery or trauma situation."},
            {"username": "alex_chen", "first_name": "Alex", "last_name": "Chen", "email": "alex.c@example.com", "blood_group": "A+", "phone": "+1 555-0143", "city": "Los Angeles", "total": 3, "days_ago": 45, "bio": "Regular donor at UCLA Medical Center. Ready to travel within LA area."},
            {"username": "priya_sharma", "first_name": "Priya", "last_name": "Sharma", "email": "priya.s@example.com", "blood_group": "B+", "phone": "+1 555-0178", "city": "Chicago", "total": 8, "days_ago": 105, "bio": "Passionate volunteer donor. Active blood drive coordinator."},
            {"username": "david_kim", "first_name": "David", "last_name": "Kim", "email": "david.k@example.com", "blood_group": "AB+", "phone": "+1 555-0189", "city": "New York", "total": 2, "days_ago": None, "bio": "AB+ universal recipient, willing to donate plasma and platelets too."},
            {"username": "elena_rostova", "first_name": "Elena", "last_name": "Rostova", "email": "elena.r@example.com", "blood_group": "O+", "phone": "+1 555-0112", "city": "Houston", "total": 6, "days_ago": 150, "bio": "O+ regular donor available on short notice in Houston area."},
            {"username": "marcus_w", "first_name": "Marcus", "last_name": "Wright", "email": "marcus.w@example.com", "blood_group": "A-", "phone": "+1 555-0167", "city": "Phoenix", "total": 4, "days_ago": 95, "bio": "Healthy marathon runner. A- donor ready to help."},
            {"username": "fatima_al", "first_name": "Fatima", "last_name": "Al-Mansoor", "email": "fatima.a@example.com", "blood_group": "B-", "phone": "+1 555-0134", "city": "Philadelphia", "total": 7, "days_ago": 110, "bio": "B- rare group donor. Please reach out anytime for emergency cases."},
            {"username": "lucas_silva", "first_name": "Lucas", "last_name": "Silva", "email": "lucas.s@example.com", "blood_group": "AB-", "phone": "+1 555-0155", "city": "Chicago", "total": 3, "days_ago": 30, "bio": "Rare AB- blood donor."},
        ]

        created_users = []
        today = timezone.now().date()

        for data in sample_donors_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('Password123!')
                user.save()

            last_donated_date = today - timedelta(days=data['days_ago']) if data['days_ago'] else None

            DonorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'blood_group': data['blood_group'],
                    'phone': data['phone'],
                    'city': data['city'],
                    'total_donations': data['total'],
                    'last_donated': last_donated_date,
                    'bio': data['bio'],
                    'is_available': True if (data['days_ago'] is None or data['days_ago'] >= 90) else False,
                }
            )
            created_users.append(user)

        # Sample Blood Requests
        sample_requests = [
            {
                "patient_name": "Emily Watson",
                "blood_group": "O-",
                "units_needed": 3,
                "hospital": "Mount Sinai Hospital",
                "location": "New York",
                "hospital_address": "1468 Madison Ave, New York, NY 10029 (ICU Ward 3B)",
                "contact_number": "+1 555-9011",
                "alternate_contact": "+1 555-9012",
                "urgency": UrgencyLevel.CRITICAL,
                "needed_by": today + timedelta(days=1),
                "notes": "Emergency surgery for cardiac trauma patient. O- blood required urgently.",
                "is_fulfilled": False,
            },
            {
                "patient_name": "Robert Miller",
                "blood_group": "B+",
                "units_needed": 2,
                "hospital": "Northwestern Memorial Hospital",
                "location": "Chicago",
                "hospital_address": "251 E Huron St, Chicago, IL 60611",
                "contact_number": "+1 555-9033",
                "urgency": UrgencyLevel.URGENT,
                "needed_by": today + timedelta(days=2),
                "notes": "Scheduled orthopedic surgery. Need 2 units of B+ blood on standby.",
                "is_fulfilled": False,
            },
            {
                "patient_name": "Amina Begum",
                "blood_group": "A-",
                "units_needed": 2,
                "hospital": "Cedars-Sinai Medical Center",
                "location": "Los Angeles",
                "hospital_address": "8700 Beverly Blvd, Los Angeles, CA 90048",
                "contact_number": "+1 555-9044",
                "urgency": UrgencyLevel.CRITICAL,
                "needed_by": today + timedelta(days=1),
                "notes": "Postpartum hemorrhage complication. Immediate A- or O- donor required.",
                "is_fulfilled": False,
            },
            {
                "patient_name": "Carlos Gomez",
                "blood_group": "AB-",
                "units_needed": 1,
                "hospital": "Houston Methodist Hospital",
                "location": "Houston",
                "hospital_address": "6565 Fannin St, Houston, TX 77030",
                "contact_number": "+1 555-9055",
                "urgency": UrgencyLevel.STANDARD,
                "needed_by": today + timedelta(days=3),
                "notes": "Routine transfusion for thalassemia patient.",
                "is_fulfilled": False,
            },
            {
                "patient_name": "Grace Hopper",
                "blood_group": "O+",
                "units_needed": 4,
                "hospital": "Penn Presbyterian Medical Center",
                "location": "Philadelphia",
                "hospital_address": "51 N 39th St, Philadelphia, PA 19104",
                "contact_number": "+1 555-9066",
                "urgency": UrgencyLevel.URGENT,
                "needed_by": today + timedelta(days=2),
                "notes": "Multiple trauma accident case. Surgery scheduled tomorrow morning.",
                "is_fulfilled": False,
            },
            {
                "patient_name": "James Wilson",
                "blood_group": "A+",
                "units_needed": 1,
                "hospital": "City General Hospital",
                "location": "New York",
                "hospital_address": "Room 402, Building A",
                "contact_number": "+1 555-9077",
                "urgency": UrgencyLevel.STANDARD,
                "needed_by": today - timedelta(days=5),
                "notes": "Pre-scheduled minor procedure.",
                "is_fulfilled": True,
            }
        ]

        # Use first created user as requester or create an admin requester
        requester_user = created_users[0] if created_users else User.objects.first()

        for req_data in sample_requests:
            BloodRequest.objects.update_or_create(
                patient_name=req_data['patient_name'],
                hospital=req_data['hospital'],
                defaults={
                    'requester': requester_user,
                    'blood_group': req_data['blood_group'],
                    'units_needed': req_data['units_needed'],
                    'location': req_data['location'],
                    'hospital_address': req_data.get('hospital_address', ''),
                    'contact_number': req_data['contact_number'],
                    'alternate_contact': req_data.get('alternate_contact', ''),
                    'urgency': req_data['urgency'],
                    'needed_by': req_data.get('needed_by'),
                    'notes': req_data.get('notes', ''),
                    'is_fulfilled': req_data['is_fulfilled'],
                }
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(sample_donors_data)} donors and {len(sample_requests)} blood requests!"))
