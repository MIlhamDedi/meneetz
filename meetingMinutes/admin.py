from django.contrib import admin

# Register your models here.
from .models import MeetingMinute
from .forms import MeetingMinuteForm

class MeetingMinuteAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'id'
    ]
    # readonly_fields = ['id', 'meeting_transcript', 'created_on']
    form = MeetingMinuteForm

admin.site.register(MeetingMinute, MeetingMinuteAdmin)
