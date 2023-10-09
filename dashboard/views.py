from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def about(request):
    return render(request, 'dashboard/about.html')

@login_required
def events(request):
    return render(request, 'dashboard/events.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

