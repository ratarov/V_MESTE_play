# Generated by Django 3.2 on 2023-01-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_meeting_banned_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='icons', verbose_name='Иконка')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
