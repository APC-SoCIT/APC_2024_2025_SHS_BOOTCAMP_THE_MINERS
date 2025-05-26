from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'dashboard/homepage.html')

def login_view(request):
    return render(request, 'dashboard/login.html')

def tutor(request):
    return render(request, 'dashboard/tutor.html')