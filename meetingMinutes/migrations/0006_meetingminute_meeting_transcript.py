# Generated by Django 2.1.5 on 2019-02-06 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetingMinutes', '0005_auto_20190205_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingminute',
            name='meeting_transcript',
            field=models.TextField(blank=True, null=True),
        ),
    ]
