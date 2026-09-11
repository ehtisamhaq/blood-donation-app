from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Blood Requests
    path('requests/', views.requests_list_view, name='requests_list'),
    path('requests/new/', views.create_request_view, name='create_request'),
    path('requests/<int:pk>/', views.request_detail_view, name='request_detail'),
    path('requests/<int:pk>/edit/', views.edit_request_view, name='edit_request'),
    path('requests/<int:pk>/toggle-fulfill/', views.toggle_fulfill_request_view, name='toggle_fulfill_request'),

    # Donors Directory
    path('donors/', views.donors_list_view, name='donors_list'),
    path('donors/<int:pk>/', views.donor_detail_view, name='donor_detail'),

    # Guide
    path('guide/', views.guide_view, name='guide'),

    # Authentication & Profile
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
