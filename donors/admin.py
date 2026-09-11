from django.contrib import admin
from .models import DonorProfile, BloodRequest

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'phone', 'city', 'is_available', 'last_donated', 'total_donations', 'is_eligible_display')
    list_filter = ('blood_group', 'is_available', 'city')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'city', 'address')
    list_editable = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(boolean=True, description='Eligible?')
    def is_eligible_display(self, obj):
        return obj.is_eligible_to_donate

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'units_needed', 'hospital', 'location', 'urgency', 'is_fulfilled', 'created_at')
    list_filter = ('blood_group', 'urgency', 'is_fulfilled', 'location')
    search_fields = ('patient_name', 'hospital', 'location', 'contact_number', 'notes')
    list_editable = ('is_fulfilled',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_fulfilled', 'mark_as_urgent']

    @admin.action(description="Mark selected requests as fulfilled")
    def mark_as_fulfilled(self, request, queryset):
        queryset.update(is_fulfilled=True)

    @admin.action(description="Mark selected requests as Urgent")
    def mark_as_urgent(self, request, queryset):
        queryset.update(urgency='URGENT')
