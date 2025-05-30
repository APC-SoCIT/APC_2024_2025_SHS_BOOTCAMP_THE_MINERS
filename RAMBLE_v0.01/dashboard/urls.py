from django.urls import path
from . import views

urlpatterns = [
    path('tutors/', views.tutor, name='tutor'),
    path('tutor/<int:tutor_id>/', views.tutor_profile, name='tutor_profile'),
]