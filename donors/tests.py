from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import DonorProfile, BloodRequest, BloodGroup, UrgencyLevel

class DonorModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testdonor',
            password='TestPassword123!',
            first_name='Jane',
            last_name='Doe'
        )
        self.profile = DonorProfile.objects.create(
            user=self.user,
            blood_group=BloodGroup.O_NEGATIVE,
            phone='+1 555-0100',
            city='Boston',
            total_donations=3,
            last_donated=timezone.now().date() - timedelta(days=100)
        )

    def test_donor_str(self):
        self.assertEqual(str(self.profile), "Jane Doe (O-) - Boston")

    def test_donor_eligibility_true(self):
        self.assertTrue(self.profile.is_eligible_to_donate)
        self.assertEqual(self.profile.days_until_eligible, 0)

    def test_donor_eligibility_cooldown(self):
        self.profile.last_donated = timezone.now().date() - timedelta(days=30)
        self.profile.save()
        self.assertFalse(self.profile.is_eligible_to_donate)
        self.assertGreater(self.profile.days_until_eligible, 0)


class BloodRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='requester',
            password='Password123!'
        )
        self.request_obj = BloodRequest.objects.create(
            requester=self.user,
            patient_name='Alice Smith',
            blood_group=BloodGroup.A_POSITIVE,
            units_needed=2,
            hospital='City Hospital',
            location='Boston',
            contact_number='+1 555-0200',
            urgency=UrgencyLevel.CRITICAL
        )

    def test_request_str(self):
        self.assertIn("Alice Smith", str(self.request_obj))
        self.assertIn("A+", str(self.request_obj))

    def test_default_unfulfilled(self):
        self.assertFalse(self.request_obj.is_fulfilled)


class ViewsIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='john_doe',
            password='Password123!',
            first_name='John',
            last_name='Doe'
        )
        self.profile = DonorProfile.objects.create(
            user=self.user,
            blood_group=BloodGroup.B_POSITIVE,
            phone='+1 555-0300',
            city='Seattle'
        )
        self.blood_req = BloodRequest.objects.create(
            requester=self.user,
            patient_name='Bob Brown',
            blood_group=BloodGroup.B_POSITIVE,
            units_needed=1,
            hospital='Swedish Medical',
            location='Seattle',
            contact_number='+1 555-0300',
            urgency=UrgencyLevel.URGENT
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RedPulse')
        self.assertContains(response, 'Swedish Medical')

    def test_requests_list_view(self):
        response = self.client.get(reverse('requests_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob Brown')

    def test_requests_list_filter(self):
        response = self.client.get(reverse('requests_list') + '?blood_group=O-')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Bob Brown')

    def test_request_detail_view(self):
        response = self.client.get(reverse('request_detail', kwargs={'pk': self.blood_req.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob Brown')
        self.assertContains(response, 'Swedish Medical')

    def test_donors_list_view(self):
        response = self.client.get(reverse('donors_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_donor_detail_view(self):
        response = self.client.get(reverse('donor_detail', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_register_flow(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Mary',
            'last_name': 'Jane',
            'username': 'maryjane',
            'email': 'mary@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
            'blood_group': 'O+',
            'phone': '+1 555-0999',
            'city': 'Miami',
            'address': 'South Beach',
            'is_available': True,
        })
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(username='maryjane').exists())
        self.assertTrue(DonorProfile.objects.filter(user__username='maryjane').exists())

    def test_create_request_view_authenticated(self):
        self.client.login(username='john_doe', password='Password123!')
        response = self.client.post(reverse('create_request'), {
            'patient_name': 'Michael Jordan',
            'blood_group': 'AB+',
            'units_needed': 2,
            'urgency': 'CRITICAL',
            'hospital': 'Chicago Hospital',
            'location': 'Chicago',
            'contact_number': '+1 555-2323',
        })
        created_req = BloodRequest.objects.filter(patient_name='Michael Jordan').first()
        self.assertIsNotNone(created_req)
        self.assertRedirects(response, reverse('request_detail', kwargs={'pk': created_req.pk}))

    def test_toggle_fulfill_request(self):
        self.client.login(username='john_doe', password='Password123!')
        self.assertFalse(self.blood_req.is_fulfilled)
        response = self.client.get(reverse('toggle_fulfill_request', kwargs={'pk': self.blood_req.pk}))
        self.blood_req.refresh_from_db()
        self.assertTrue(self.blood_req.is_fulfilled)
