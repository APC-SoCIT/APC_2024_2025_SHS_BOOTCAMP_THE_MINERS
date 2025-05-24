from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'dashboard/login.html')

def homepage(request):
    return render(request, 'dashboard/homepage.html')