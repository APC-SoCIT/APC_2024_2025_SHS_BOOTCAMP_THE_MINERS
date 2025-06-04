"""
This is the URL configuration for the dashboard app.
It defines routes specific to dashboard features (tutors, bookings, etc).
These are included in the main project URLs via `include('dashboard.urls')`.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('tutors/', views.tutor, name='tutor'),
    path('tutors/subject/<int:subject_id>/', views.tutor_by_subject, name='tutor_by_subject'),
    path('tutor/<int:tutor_id>/', views.profile, name='tutor_profile'),
    path('tutor/<int:tutor_id>/book/', views.book_tutor, name='book_tutor'),
    path('tutor/bookings/', views.tutor_bookings, name='tutor_bookings'),
]