from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import SignUpForm

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
def profile(request):
    return render(request, 'dashboard/profile.html')

def ramble_wizard(request):
    return render(request, 'dashboard/ramble-wizard.html')

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user object but don't save yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save user to database
            login(request, user)  # Log the user in
            return redirect('homepage')  # Redirect to homepage
    else:
        form = SignUpForm()
    return render(request, 'dashboard/sign_up.html', {'form': form})

def tutor(request):
    return render(request, 'dashboard/tutor.html')