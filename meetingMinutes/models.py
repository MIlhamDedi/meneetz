from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MeetingMinute(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=240, verbose_name='Meeting Title', unique=True, help_text='Must be a unique title.')
    created_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voice_recording_file = models.FileField(upload_to=user_directory_path, verbose_name='Voice Recording File')

    class Meta:
        verbose_name = 'Meeting Minute'
        verbose_name_plural = 'Meeting Minutes'

    def __str__(self):
        return self.title
