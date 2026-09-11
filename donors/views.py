from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import DonorProfile, BloodRequest, BloodGroup, UrgencyLevel
from .forms import (
    DonorRegistrationForm,
    UserLoginForm,
    BloodRequestForm,
    DonorProfileUpdateForm
)


def home_view(request):
    """Landing page with statistics, urgent emergency ticker, and quick search."""
    # Stats
    total_donors = DonorProfile.objects.count()
    available_donors = DonorProfile.objects.filter(is_available=True).count()
    active_requests_count = BloodRequest.objects.filter(is_fulfilled=False).count()
    fulfilled_requests_count = BloodRequest.objects.filter(is_fulfilled=True).count()
    
    # Recent emergency blood requests (unfulfilled first, order by urgency and date)
    recent_requests = BloodRequest.objects.filter(is_fulfilled=False).order_by(
        '-created_at'
    )[:6]

    # Featured available donors
    featured_donors = DonorProfile.objects.filter(is_available=True).select_related('user')[:4]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'active_requests_count': active_requests_count,
        'fulfilled_requests_count': fulfilled_requests_count,
        'recent_requests': recent_requests,
        'featured_donors': featured_donors,
        'blood_groups': BloodGroup.choices,
    }
    return render(request, 'donors/home.html', context)


def requests_list_view(request):
    """Urgent and active blood requests feed with search and multi-filtering."""
    query = request.GET.get('q', '').strip()
    blood_group = request.GET.get('blood_group', '').strip()
    urgency = request.GET.get('urgency', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', 'active').strip()
    date_range = request.GET.get('date_range', '').strip()

    requests_qs = BloodRequest.objects.select_related('requester').all()

    if status == 'active':
        requests_qs = requests_qs.filter(is_fulfilled=False)
    elif status == 'fulfilled':
        requests_qs = requests_qs.filter(is_fulfilled=True)

    if blood_group:
        requests_qs = requests_qs.filter(blood_group=blood_group)

    if urgency:
        requests_qs = requests_qs.filter(urgency=urgency)

    if location:
        requests_qs = requests_qs.filter(
            Q(location__icontains=location) | Q(hospital__icontains=location)
        )
    
    if date_range == '24h':
        requests_qs = requests_qs.filter(created_at__gte=timezone.now() - timedelta(hours=24))
    elif date_range == '3d':
        requests_qs = requests_qs.filter(created_at__gte=timezone.now() - timedelta(days=3))

    if query:
        requests_qs = requests_qs.filter(
            Q(patient_name__icontains=query) |
            Q(hospital__icontains=query) |
            Q(location__icontains=query) |
            Q(notes__icontains=query)
        )

    requests_qs = requests_qs.order_by('is_fulfilled', '-created_at')

    paginator = Paginator(requests_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'blood_group': blood_group,
        'urgency': urgency,
        'location': location,
        'status': status,
        'date_range': date_range,
        'blood_groups': BloodGroup.choices,
        'urgency_levels': UrgencyLevel.choices,
        'total_count': requests_qs.count(),
    }
    return render(request, 'donors/requests_list.html', context)


def request_detail_view(request, pk):
    """Detailed view for a single emergency blood request."""
    blood_req = get_object_or_404(BloodRequest.objects.select_related('requester'), pk=pk)

    # Find matching available donors in the same blood group or universal donors
    matching_donors = DonorProfile.objects.filter(
        blood_group=blood_req.blood_group,
        is_available=True
    ).select_related('user')[:5]

    context = {
        'request_item': blood_req,
        'matching_donors': matching_donors,
    }
    return render(request, 'donors/request_detail.html', context)


@login_required(login_url='login')
def create_request_view(request):
    """Submit a new urgent blood request."""
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_req = form.save(commit=False)
            blood_req.requester = request.user
            blood_req.save()
            messages.success(request, f"Blood request for {blood_req.patient_name} ({blood_req.blood_group}) posted successfully!")
            return redirect('request_detail', pk=blood_req.pk)
    else:
        # Prepopulate contact number if user has donor profile
        initial = {}
        if hasattr(request.user, 'donor_profile'):
            initial['contact_number'] = request.user.donor_profile.phone
            initial['location'] = request.user.donor_profile.city
        form = BloodRequestForm(initial=initial)

    context = {
        'form': form,
        'page_title': 'Post Urgent Blood Request',
        'is_edit': False,
    }
    return render(request, 'donors/request_form.html', context)


@login_required(login_url='login')
def edit_request_view(request, pk):
    """Edit an existing blood request (only by creator)."""
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if blood_req.requester != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this request.")
        return redirect('request_detail', pk=pk)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_req)
        if form.is_valid():
            form.save()
            messages.success(request, "Blood request updated successfully.")
            return redirect('request_detail', pk=blood_req.pk)
    else:
        form = BloodRequestForm(instance=blood_req)

    context = {
        'form': form,
        'page_title': f"Edit Request for {blood_req.patient_name}",
        'is_edit': True,
        'blood_req': blood_req,
    }
    return render(request, 'donors/request_form.html', context)


@login_required(login_url='login')
def toggle_fulfill_request_view(request, pk):
    """Toggle fulfilled status of a blood request."""
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if blood_req.requester != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to modify this request.")
        return redirect('request_detail', pk=pk)

    blood_req.is_fulfilled = not blood_req.is_fulfilled
    blood_req.save()

    status_text = "marked as fulfilled" if blood_req.is_fulfilled else "re-opened as active"
    messages.success(request, f"Request {status_text}.")
    return redirect('request_detail', pk=pk)


def donors_list_view(request):
    """Search and filter registered blood donors."""
    query = request.GET.get('q', '').strip()
    blood_group = request.GET.get('blood_group', '').strip()
    city = request.GET.get('city', '').strip()
    available_only = request.GET.get('available_only', '1').strip()

    donors_qs = DonorProfile.objects.select_related('user').all()

    if available_only == '1':
        donors_qs = donors_qs.filter(is_available=True)

    if blood_group:
        donors_qs = donors_qs.filter(blood_group=blood_group)

    if city:
        donors_qs = donors_qs.filter(city__icontains=city)

    if query:
        donors_qs = donors_qs.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(city__icontains=query) |
            Q(bio__icontains=query)
        )

    # Order by available first, total donations, then recency
    donors_qs = donors_qs.order_by('-is_available', '-total_donations', '-created_at')

    paginator = Paginator(donors_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get distinct cities for filter dropdown/datalist
    popular_cities = DonorProfile.objects.values_list('city', flat=True).distinct()[:10]

    context = {
        'page_obj': page_obj,
        'query': query,
        'blood_group': blood_group,
        'city': city,
        'available_only': available_only,
        'blood_groups': BloodGroup.choices,
        'popular_cities': popular_cities,
        'total_donors': donors_qs.count(),
    }
    return render(request, 'donors/donors_list.html', context)


def donor_detail_view(request, pk):
    """Public profile view for an individual donor."""
    donor = get_object_or_404(DonorProfile.objects.select_related('user'), pk=pk)
    context = {
        'donor': donor,
    }
    return render(request, 'donors/donor_detail.html', context)


def guide_view(request):
    """User guide for the platform."""
    return render(request, 'donors/guide.html')


def register_view(request):
    """Register a new user and donor profile in one seamless flow."""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Create Donor Profile
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            # Auto log in
            login(request, user)
            messages.success(request, f"Welcome to the platform, {user.first_name}! You are registered as a {profile.blood_group} donor.")
            return redirect('profile')
    else:
        form = DonorRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'donors/register.html', context)


def login_view(request):
    """Login existing user."""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'donors/login.html', context)


def logout_view(request):
    """Logout current user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    """User profile dashboard to manage donor details and view posted requests."""
    user = request.user
    donor_profile, created = DonorProfile.objects.get_or_create(
        user=user,
        defaults={
            'blood_group': BloodGroup.O_POSITIVE,
            'phone': '',
            'city': 'Unknown'
        }
    )

    if request.method == 'POST':
        form = DonorProfileUpdateForm(request.POST, instance=donor_profile)
        if form.is_valid():
            # Update User fields
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save Profile
            form.save()
            messages.success(request, "Profile information updated successfully!")
            return redirect('profile')
    else:
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = DonorProfileUpdateForm(instance=donor_profile, initial=initial)

    # User's submitted blood requests
    user_requests = BloodRequest.objects.filter(requester=user).order_by('-created_at')

    context = {
        'form': form,
        'donor_profile': donor_profile,
        'user_requests': user_requests,
    }
    return render(request, 'donors/profile.html', context)