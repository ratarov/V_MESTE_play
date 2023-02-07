# Generated by Django 3.2 on 2023-01-28 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0008_meeting_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='outside_players',
        ),
        migrations.CreateModel(
            name='MeetingPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.PositiveSmallIntegerField(default=0, verbose_name='Количество гостей')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='meetings.meeting')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Участик встречи',
                'verbose_name_plural': 'Участники встречи',
            },
        ),
        # migrations.AlterField(
        #     model_name='meeting',
        #     name='site_players',
        #     field=models.ManyToManyField(blank=True, related_name='played', through='meetings.MeetingPlayer', to=settings.AUTH_USER_MODEL),
        # ),
        migrations.AddConstraint(
            model_name='meetingplayer',
            constraint=models.UniqueConstraint(fields=('meeting', 'player'), name='unique_participant'),
        ),
    ]
