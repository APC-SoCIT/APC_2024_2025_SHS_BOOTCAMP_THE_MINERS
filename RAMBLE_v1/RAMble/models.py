from django.db import models
from django.contrib.auth.models import User

# Create your models here.  
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Tutor(models.Model):
    # Connect Tutor to a Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional tutor-specific fields
    full_name = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0) 
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    subjects = models.ManyToManyField(Subject, related_name='tutors')
    about = models.TextField(blank=True, default='This tutor has not added a description yet.')

    def __str__(self):
        return self.full_name
    
    
class Booking(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class TutorAvailability(models.Model):
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    time_slot = models.TimeField(null=True, blank=True) 
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('tutor', 'date', 'time_slot')
        
    def __str__(self):
        return f"{self.tutor.full_name} - {self.date} {self.time_slot or ''}"
