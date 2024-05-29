from django import forms
from django.contrib.auth.forms import UserCreationForm
from Bus.models import LostItem, ViolationReport, FreeBoardPost, BusRequest
from datetime import date, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()  # 동적으로 사용자 모델 가져오기

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

class BusRequestForm(forms.ModelForm):
    class Meta:
        model = BusRequest
        fields = ['destination', 'date', 'time', 'reason']
    ''' widgets = {
            'user': forms.HiddenInput(),  # 숨겨진 입력 필드로 설정
        }'''

    DESTINATIONS = [
        ('seoul', '서울행'),
        ('suwon', '수원행'), 
    ]
    TIMES = {
        'seoul': [
            ('07:00', '07:00'),
            ('10:30', '10:30'),
            ('12:00', '12:00'),
            ('13:30', '13:30'),
            ('15:00', '15:00'),
            ('16:30', '16:30'),
            ('18:15', '18:15'),
        ],
        'seoul_friday': [
            ('08:00', '08:00'),
            ('10:30', '10:30'),
            ('12:00', '12:00'),
            ('13:30', '13:30'),
            ('15:00', '15:00'),
            ('16:30', '16:30'),
            ('18:15', '18:15'),
        ],
        'suwon': [
            ('07:00', '07:00'),
            ('10:00', '10:00'),
            ('12:00', '12:00'),
            ('15:00', '15:00'),
            ('16:30', '16:30'),
            ('18:00', '18:00'),
            ('19:00', '19:00'),
        ],
        'suwon_friday': [
            ('08:00', '08:00'),
            ('10:00', '10:00'),
            ('12:00', '12:00'),
            ('15:00', '15:00'),
            ('16:30', '16:30'),
            ('18:00', '18:00'),
            ('19:00', '19:00'),
        ],
    }
    destination = forms.ChoiceField(choices=DESTINATIONS)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.ChoiceField(choices=TIMES['seoul'])  # 기본값으로 서울 시간대 설정
    reason = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(BusRequestForm, self).__init__(*args, **kwargs)
        today = date.today()
        max_date = today + timedelta(days=3)
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        self.fields['date'].widget.attrs['max'] = max_date.strftime('%Y-%m-%d')
        valid_dates = [today + timedelta(days=i) for i in range(4) if (today + timedelta(days=i)).weekday() < 5]
        valid_dates_str = [d.strftime('%Y-%m-%d') for d in valid_dates]
        self.fields['date'].widget.attrs['valid_dates'] = valid_dates_str

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