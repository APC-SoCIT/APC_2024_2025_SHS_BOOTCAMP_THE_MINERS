from django.contrib import admin
from .models import Tutor, Subject, TutorAvailability
# Register your models here.

admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(TutorAvailability)

