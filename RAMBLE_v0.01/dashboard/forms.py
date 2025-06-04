from django import forms
from django.contrib.auth.models import User
from RAMble.models import Subject

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    is_tutor = forms.BooleanField(required=False, label='Register as Tutor')
    rate_per_hour = forms.DecimalField(required=False, min_value=0, label='Rate per hour')
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label='Subjects you wish to teach'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")
        if cleaned_data.get('is_tutor'):
            if not cleaned_data.get('rate_per_hour'):
                self.add_error('rate_per_hour', "Rate per hour is required for tutors.")
            if not cleaned_data.get('subjects'):
                self.add_error('subjects', "Please select at least one subject.")
        return cleaned_data