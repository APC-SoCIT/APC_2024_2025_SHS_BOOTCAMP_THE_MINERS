from django.contrib import admin
from .models import Tutor, Subject, TutorAvailability
# Register your models here.

admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(TutorAvailability)

class TutorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'rating', 'rate_per_hour')
    fields = ('full_name', 'email', 'rating', 'rate_per_hour', 'subjects', 'about', 'profile_picture')