from django.contrib import admin
from .models import NoShow, User

class NoShowAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'reason')
    search_fields = ('user__student_id', 'date')

admin.site.register(NoShow, NoShowAdmin)
admin.site.register(User)
