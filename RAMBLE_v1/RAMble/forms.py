from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',  # Keep type as 'date'
                'class': 'calendar-input',  # Add custom class for styling
                'placeholder': 'Select a date',  # Add placeholder for better UX
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',  # Keep type as 'time'
                'class': 'time-input',  # Add custom class for styling
                'placeholder': 'Select a time',  # Add placeholder for better UX
            }),
        }