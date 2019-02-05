from django import forms
from .models import MeetingMinute

class MeetingMinuteForm(forms.ModelForm):
    class Meta:
        model = MeetingMinute
        fields = ['title, created_on, voice_recording_file']
