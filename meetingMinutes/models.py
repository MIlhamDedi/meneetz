import json
import os
import subprocess

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.utils.text import slugify

recog_config = speech.types.RecognitionConfig(
    model='video',
    language_code='en-US',
    enable_automatic_punctuation=True,
    enable_speaker_diarization=True,
    diarization_speaker_count=2
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MeetingMinute(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=240, verbose_name='Meeting Title', unique=True, help_text='Must be a unique title.')
    created_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voice_recording_file = models.FileField(upload_to=user_directory_path, verbose_name='Voice Recording File')
    meeting_transcript = models.TextField(null=True, blank=True, verbose_name='Meeting Transcript')

    class Meta:
        verbose_name = 'Meeting Minute'
        verbose_name_plural = 'Meeting Minutes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meeting_minute_detail', kwargs={'pk': int(self.id)})

# invoke the google cloud speech-to-text api
def post_save_minute(sender, instance, created, update_fields=['meeting_transcript'], **kwargs):
    # instantiates a client
    client = speech.SpeechClient()

    # convert file to FLAC format
    voice_file_path = os.path.join(settings.MEDIA_ROOT, str(instance.voice_recording_file))
    flac_file_name = str(instance.voice_recording_file).split('.')[0] + '.flac'
    flac_file_path = os.path.join(settings.MEDIA_ROOT, flac_file_name)
    convert_cmd = 'ffmpeg -i {} {}'.format(voice_file_path, flac_file_path)
    subprocess.run(convert_cmd, shell=True)

    # loads the audio into memory
    with open(flac_file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.types.RecognitionAudio(content=content)

    # detects speech in the audio file
    response = client.recognize(recog_config, audio)

    # Last transcript contains all the world. So, this is fine.
    result = response.results[-1]
    words_info = result.alternatives[0].words
    voice_transcript = ""
    speaker_tag = 0 # Random number
    for word_info in words_info:
        whitespace = ' '
        if (word_info.speaker_tag != speaker_tag):
            whitespace = '\n{}: '.format(word_info.speaker_tag)
        speaker_tag = word_info.speaker_tag
        voice_transcript += ("{}{}".format(whitespace, word_info.word))
    voice_transcript = voice_transcript.lstrip()
    json_voice_transcript = []
    for line in voice_transcript.split('\n'):
        json_voice_transcript.append({"id":line.split(":", 1)[0], "msg": line.split(":",1)[1].lstrip()})
    json_voice_transcript = json.dumps(json_voice_transcript)

    # print(voice_transcript)

    # update the meeting transcript for the meeting
    MeetingMinute.objects.filter(id=instance.id).update(meeting_transcript=json_voice_transcript)

# pre_save.connect(pre_save_minute, sender=MeetingMinute)
post_save.connect(post_save_minute, sender=MeetingMinute)
