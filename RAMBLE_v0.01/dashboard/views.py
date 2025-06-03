from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import SignUpForm
from RAMble.models import Tutor, Subject, Booking
from django.shortcuts import get_object_or_404
from RAMble.forms import BookingForm
from django.core.mail import send_mail
from django.contrib import messages

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
    subject_id = request.GET.get('subject')
    if subject_id:
        tutors = Tutor.objects.filter(subjects__id=subject_id)
    else:
        tutors = Tutor.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {'tutors': tutors, 'subjects': subjects})

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

def tutor_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    tutors = Tutor.objects.filter(subjects=subject)
    subjects = Subject.objects.all()
    return render(request, 'dashboard/tutor.html', {
        'tutors': tutors,
        'subjects': subjects,
        'selected_subject': subject,
    })

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
            send_mail(
                'New Booking Request',
                f'You have a new booking request from {request.user.username} for {booking.date} at {booking.time}.',
                'noreply@ramble.com',
                [tutor.user.email],
            )
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'dashboard/book_tutor.html', {'form': form, 'tutor': tutor})

@login_required
def tutor_bookings(request):
    # Assumes the logged-in user is a Tutor (adjust as needed)
    tutor = request.user.tutor
    bookings = Booking.objects.filter(tutor=tutor).order_by('-created_at')
    return render(request, 'dashboard/tutor_bookings.html', {'bookings': bookings})