from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@g.skku.edu'):
            raise forms.ValidationError('Email must be a SKKU email address')
        return email
