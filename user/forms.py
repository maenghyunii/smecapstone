from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    student_id = forms.CharField(max_length=10, required=True, help_text="Enter your student ID.")
    name = forms.CharField(max_length=100, required=True, help_text="Enter your name.")
    class Meta:
        model = User
        fields = ('email', 'student_id', 'name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@g.skku.edu'):
            raise forms.ValidationError('Email must be a SKKU email address')
        return email
