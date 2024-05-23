from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Bus.models import LostItem, ViolationReport, FreeBoardPost

class CustomUserCreationForm(UserCreationForm):
    student_id = forms.CharField(max_length=15, required=True)
    name = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('email', 'student_id', 'name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith(('@g.skku.edu', '@skku.edu')):
            raise forms.ValidationError('Email must be a SKKU email address')
        return email


class BusRequestForm(forms.Form):
    DESTINATIONS = [
        ('suwon', '수원행'),
        ('seoul', '서울행'),
    ]

    destination = forms.ChoiceField(choices=DESTINATIONS)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    reason = forms.CharField(widget=forms.Textarea)

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'content']

class ViolationReportForm(forms.ModelForm):
    class Meta:
        model = ViolationReport
        fields = ['title', 'content']

class FreeBoardPostForm(forms.ModelForm):
    class Meta:
        model = FreeBoardPost
        fields = ['title', 'content']