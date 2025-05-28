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
"""
from django.contrib import admin
from django.urls import path, include
# kurt added these
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Show login page first when opening 127.0.0.1:8000/
    path('homepage/', views.homepage, name='homepage'),  # Redirect here after login
    path('tutor/', views.tutor, name='tutor'),
    path('profile/', views.profile, name='profile'),
    path('ramble_wizard/', views.ramble_wizard, name='ramble_wizard'),
    path('sign_up/', views.sign_up, name='sign_up'),  # Include URLs from the RAMble app
]

