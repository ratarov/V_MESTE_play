# Generated by Django 3.2 on 2023-01-30 10:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0015_auto_20230130_1309'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MeetingPlayer',
            new_name='MeetingParticipation',
        ),
    ]
