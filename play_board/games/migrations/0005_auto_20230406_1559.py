# Generated by Django 3.2 on 2023-04-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_game_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name_eng',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='name_rus',
            field=models.TextField(null=True),
        ),
    ]
