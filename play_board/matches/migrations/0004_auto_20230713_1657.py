# Generated by Django 3.2.18 on 2023-07-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_auto_20230713_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='username',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='type',
            field=models.CharField(choices=[('PvP', 'Игрок vs Игрока'), ('PvG', 'Игрок vs Игры')], default='PvP', max_length=20),
        ),
    ]
