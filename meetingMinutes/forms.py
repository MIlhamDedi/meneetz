from django import forms
from .models import MeetingMinute

class MeetingMinuteForm(forms.ModelForm):
    class Meta:
        model = MeetingMinute
        fields = ['title', 'voice_recording_file', 'speaker_count']
        readonly_fields = ['user']
