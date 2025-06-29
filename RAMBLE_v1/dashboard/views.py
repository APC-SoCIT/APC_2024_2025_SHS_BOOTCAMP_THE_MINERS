from django.shortcuts import render, redirect, get_object_or_404  # For rendering templates and redirects
from django.contrib.auth import authenticate, login, logout  # For user authentication
from django.contrib.auth.decorators import login_required  # To restrict views to logged-in users
from django.contrib.auth.models import User  # Django's built-in user model
from .forms import SignUpForm  # Custom sign-up form for user registration (in dashboard/forms.py)
from RAMble.models import Tutor, Subject, Booking  # Main app models (in RAMble/models.py)
from RAMble.forms import BookingForm  # Booking form (in RAMble/forms.py)
from django.core.mail import send_mail  # For sending emails (e.g., booking notifications)
from django.contrib import messages  # For displaying one-time notifications to users

# --- Homepage view ---
def homepage(request):
    # Renders the main dashboard homepage
    return render(request, 'dashboard/homepage.html')

# --- Login view ---
def login_view(request):
    # Handles user login. If the user is a tutor, redirect to bookings page.
    error = None
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            # If user is a tutor, redirect to their bookings dashboard
            if Tutor.objects.filter(user=user).exists():
                return redirect('tutor_bookings')
            else:
                return redirect('homepage')  # Default for students/others
        else:
            error = "Invalid credentials"
    return render(request, 'dashboard/login.html', {'error': error})

# --- User profile page (for dropdown) ---
@login_required
def user_profile(request):
    return render(request, 'dashboard/user-profile.html')

# tutor profile page (for booking etc.) 
def profile(request, tutor_id=None):
    # shows a tutors profile and handles booking form submission on the same page
    tutor = get_object_or_404(Tutor, id=tutor_id) if tutor_id else None
    if request.method == 'POST' and tutor:
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tutor = tutor
            booking.student = request.user
            booking.save()
            messages.success(request, "Booking request sent!")
            return redirect('profile', tutor_id=tutor.id)
    else:
        form = BookingForm()
    return render(request, 'dashboard/profile.html', {'tutor': tutor, 'form': form})

# --- RAMble Wizard chatbot page ---
def ramble_wizard(request):
    return render(request, 'dashboard/ramble_wizard.html')

# --- User sign-up view ---
def sign_up(request):
    # Handles user registration
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # create user object but don't save yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            if form.cleaned_data.get('is_tutor'):
                tutor = Tutor.objects.create(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}",
                    rate_per_hour=form.cleaned_data.get('rate_per_hour')
                )
                tutor.subjects.set(form.cleaned_data.get('subjects'))
            login(request, user)  # Log the user in
            return redirect('homepage')  # Redirect to homepage
    else:
        form = SignUpForm()
    return render(request, 'dashboard/sign_up.html', {'form': form})

# --- Tutor list view ---
def tutor(request):
    # Shows all tutors, or filters by subject if provided
    subject_id = request.GET.get('subject')
    if subject_id:
        tutors = Tutor.objects.filter(subjects__id=subject_id)
    else:
        tutors = Tutor.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {'tutors': tutors, 'subjects': subjects})

# --- Tutors by subject view ---
def tutor_by_subject(request, subject_id):
    # Shows tutors filtered by a specific subject
    subject = get_object_or_404(Subject, id=subject_id)
    tutors = Tutor.objects.filter(subjects=subject)
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {
        'tutors': tutors,
        'subjects': subjects,
        'selected_subject': subject,
    })

def faqs_page(request):
    return render(request, 'dashboard/FAQs_page.html')

# --- Book a tutor (separate booking page, not used if booking is on profile page) ---
@login_required
def book_tutor(request, tutor_id):
    # Handles booking a tutor from a dedicated booking page
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tutor = tutor
            booking.student = request.user
            booking.save()
            # Removed email sending
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'dashboard/book_tutor.html', {'form': form, 'tutor': tutor})

# --- Tutor's bookings dashboard ---
@login_required
def tutor_bookings(request):
    # Shows all bookings for the currently logged-in tutor
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        return redirect('homepage')
    # Handle accept/decline POST
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