from django.shortcuts import render

# Create your views here.

from .models import BloodRequest

def home_view(request):
    # Fetch recent urgent blood requests
    recent_requests = BloodRequest.objects.filter(is_fulfilled=False).order_by('-created_at')[:5]
    
    context = {
        'recent_requests': recent_requests,
    }
    return render(request, 'donors/home.html', context)