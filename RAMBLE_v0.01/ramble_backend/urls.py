"""
URL configuration for ramble_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

This is the main URL configuration for your Django project.
It routes incoming HTTP requests to the correct app-level URLs or views.
- This file is referenced by your project's WSGI/ASGI entry point.
- It can include URLs from any app using `include()`.
- It is the first place Django looks for URL patterns.
"""

from django.contrib import admin
from django.urls import path, include
from dashboard import views  # Import views for direct mapping

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('', views.login_view, name='login'),  # Default: login page
    path('homepage/', views.homepage, name='homepage'),  # Homepage after login
    path('tutor/', views.tutor, name='tutor'),  # List of tutors
    path('profile/', views.profile, name='profile'),  # User profile
    path('ramble_wizard/', views.ramble_wizard, name='ramble_wizard'),  # Chatbot
    path('sign_up/', views.sign_up, name='sign_up'),  # Registration
    path('', include('dashboard.urls')),  # Include all URLs from the dashboard app
]