# Generated by Django 3.2 on 2023-01-29 10:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0010_auto_20230128_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='site_players',
            field=models.ManyToManyField(blank=True, related_name='played', through='meetings.MeetingPlayer', to=settings.AUTH_USER_MODEL),
        ),
    ]
