from django.contrib import admin
from django import forms
from .models import Book, NoShow, User

class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'departure_time': forms.TimeInput(format='%H:%M')
        }

class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('user', 'destination', 'departure_date', 'departure_time', 'seat')
    search_fields = ('user__student_id', 'destination', 'departure_date')

admin.site.register(Book, BookAdmin)

# 기존 코드 유지
class NoShowAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'reason')
    search_fields = ('user__student_id', 'date')

admin.site.register(NoShow, NoShowAdmin)
admin.site.register(User)
