# Generated by Django 3.2 on 2023-01-21 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name': 'Игра', 'verbose_name_plural': 'Игры'},
        ),
    ]
