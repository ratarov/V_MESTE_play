# Generated by Django 3.2 on 2023-01-29 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0011_meeting_site_players'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='banned_players',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='site_players',
        ),
    ]
