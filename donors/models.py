from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class BloodGroup(models.TextChoices):
    A_POSITIVE = 'A+', 'A+'
    A_NEGATIVE = 'A-', 'A-'
    B_POSITIVE = 'B+', 'B+'
    B_NEGATIVE = 'B-', 'B-'
    O_POSITIVE = 'O+', 'O+'
    O_NEGATIVE = 'O-', 'O-'
    AB_POSITIVE = 'AB+', 'AB+'
    AB_NEGATIVE = 'AB-', 'AB-'

class UrgencyLevel(models.TextChoices):
    CRITICAL = 'CRITICAL', 'Critical (Within hours)'
    URGENT = 'URGENT', 'Urgent (Within 24 hours)'
    STANDARD = 'STANDARD', 'Standard (Within 2-3 days)'

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, default='')
    is_available = models.BooleanField(default=True, help_text="Set whether you are currently available to donate.")
    last_donated = models.DateField(null=True, blank=True, help_text="Date of your last blood donation.")
    total_donations = models.PositiveIntegerField(default=0, help_text="Total number of completed donations.")
    bio = models.TextField(blank=True, default='', help_text="Short note or medical availability information.")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_available', '-total_donations', 'user__first_name']

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.blood_group}) - {self.city}"

    @property
    def is_eligible_to_donate(self):
        """Donors are typically eligible 90 days after last whole blood donation."""
        if not self.last_donated:
            return True
        return (timezone.now().date() - self.last_donated).days >= 90

    @property
    def days_until_eligible(self):
        if not self.last_donated:
            return 0
        days_passed = (timezone.now().date() - self.last_donated).days
        remaining = 90 - days_passed
        return max(0, remaining)

class BloodRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    units_needed = models.PositiveIntegerField(default=1, help_text="Number of blood bags/units required.")
    hospital = models.CharField(max_length=200, help_text="Name of the hospital or medical clinic.")
    location = models.CharField(max_length=200, help_text="City / District / Area")
    hospital_address = models.CharField(max_length=255, blank=True, default='', help_text="Street address or ward details")
    contact_number = models.CharField(max_length=20, help_text="Primary phone number to reach the requester/family")
    alternate_contact = models.CharField(max_length=20, blank=True, default='', help_text="Secondary contact number")
    urgency = models.CharField(max_length=10, choices=UrgencyLevel.choices, default=UrgencyLevel.URGENT)
    needed_by = models.DateField(null=True, blank=True, help_text="Target date by which blood is required.")
    notes = models.TextField(blank=True, default='', help_text="Medical details, reason for request, or instructions for donors.")
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_fulfilled', '-created_at']

    def __str__(self):
        return f"Need {self.units_needed} bag(s) of {self.blood_group} for {self.patient_name} ({self.hospital})"