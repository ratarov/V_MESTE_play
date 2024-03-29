# Generated by Django 3.2 on 2023-01-23 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_meetingstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='max_players',
            field=models.IntegerField(default=7, verbose_name='Максимальное кол-во игроков'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='meetings', to='meetings.meetingstatus'),
        ),
    ]
