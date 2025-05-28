from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.

def homepage(request):
    return render(request, 'dashboard/homepage.html')

def login_view(request):
    error = None
    if request.method == "POST":
        username_or_email = request.POST.get("username")  # meaning it can be username or email
        password = request.POST.get("password")

        # it will try looking up user by email
        user = User.objects.filter(email__iexact=username_or_email).first()
        if user:
            username = user.username  # this gets username from email
        else:
            username = username_or_email  # yung input is treated as username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error = "Invalid username or password."

    return render(request, "dashboard/login.html", {"error": error})

# def logout_view(request):
  #  logout(request)
  #  return redirect('/')  # Redirects after logout

def tutor(request):
    return render(request, 'dashboard/tutor.html')