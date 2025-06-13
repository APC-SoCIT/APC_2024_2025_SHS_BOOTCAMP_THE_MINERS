from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import SignUpForm 
from RAMble.models import Tutor, Subject, Booking 
from RAMble.forms import BookingForm 
from django.core.mail import send_mail 
from django.contrib import messages  

# --- Homepage view ---
def homepage(request):
    # Renders the main dashboard homepage
    return render(request, 'dashboard/homepage.html')

# --- Login view ---
def login_view(request):
    # Handles user login
    error = None
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            # If user is a tutor, redirect to tutor bookings
            if Tutor.objects.filter(user=user).exists():
                return redirect('tutor_bookings')
            #otherwise, redirect to homepage
            else:
                return redirect('homepage') 
        else:
            error = "Invalid credentials"
    return render(request, 'dashboard/login.html', {'error': error})

# --- Profile view
def profile(request):
    return render(request, 'dashboard/profile.html')

# --- RAMble Wizard chatbot page ---
def ramble_wizard(request):
    return render(request, 'dashboard/ramble-wizard.html')

# --- User sign-up view ---
def sign_up(request):
    # Handles user registration
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/sign_up.html', {'form': form})

# --- Tutor list view ---
def tutor(request):
    subject_id = request.GET.get('subject')
    if subject_id:
        tutors = Tutor.objects.filter(subjects__id=subject_id)
    else:
        tutors = Tutor.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {'tutors': tutors, 'subjects': subjects})

# --- tutor profile and booking form ---
def tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tutor = tutor
            booking.student = request.user
            booking.save()
            # Optionally send email here
            messages.success(request, "Booking request sent!")
            return redirect('tutor_profile', tutor_id=tutor.id)
    else:
        form = BookingForm()
    return render(request, 'dashboard/profile.html', {'tutor': tutor, 'form': form})

# --- Tutors by subject view ---
def tutor_by_subject(request, subject_id):
    # shows tutors based on filtered subject
    subject = get_object_or_404(Subject, id=subject_id)
    tutors = Tutor.objects.filter(subjects=subject)
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {
        'tutors': tutors,
        'subjects': subjects,
        'selected_subject': subject,
    })

# --- Book a tutor ---
@login_required
def book_tutor(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tutor = tutor
            booking.student = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'dashboard/book_tutor.html', {'form': form, 'tutor': tutor})

# --- Tutor's bookings dashboard ---
@login_required
def tutor_bookings(request):
    # shows all bookings for the tutor who is logged in.
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        return redirect('homepage')
    # handles the accepting and declining of bookings
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = Booking.objects.get(id=booking_id, tutor=tutor)
        if action == "accept":
            booking.status = "accepted"
        elif action == "decline":
            booking.status = "declined"
        booking.save()

    bookings = Booking.objects.filter(tutor=tutor).order_by('-created_at')
    return render(request, 'dashboard/tutor_bookings.html', {'bookings': bookings})