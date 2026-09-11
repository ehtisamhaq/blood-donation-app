from django.contrib import admin
from django.contrib.auth.models import User
from .models import DonorProfile, BloodRequest

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'phone', 'city', 'is_available', 'last_donated', 'total_donations', 'is_eligible_display', 'is_user_active')
    list_filter = ('blood_group', 'is_available', 'city', 'user__is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'city', 'address')
    list_editable = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['block_users', 'unblock_users']

    @admin.display(boolean=True, description='Eligible?')
    def is_eligible_display(self, obj):
        return obj.is_eligible_to_donate

    @admin.display(boolean=True, description='Active User')
    def is_user_active(self, obj):
        return obj.user.is_active

    @admin.action(description="Block selected users")
    def block_users(self, request, queryset):
        user_ids = queryset.values_list('user_id', flat=True)
        count = User.objects.filter(id__in=user_ids).update(is_active=False)
        self.message_user(request, f"{count} user(s) blocked.")

    @admin.action(description="Unblock selected users")
    def unblock_users(self, request, queryset):
        user_ids = queryset.values_list('user_id', flat=True)
        count = User.objects.filter(id__in=user_ids).update(is_active=True)
        self.message_user(request, f"{count} user(s) unblocked.")

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
