# Generated by Django 3.2.18 on 2023-02-21 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0016_rename_meetingplayer_meetingparticipation'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingparticipation',
            name='total_qty',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Игрок + гости'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='players',
            field=models.ManyToManyField(blank=True, through='meetings.MeetingParticipation', to=settings.AUTH_USER_MODEL),
        ),
    ]
