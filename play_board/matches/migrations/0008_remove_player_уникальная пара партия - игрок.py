# Generated by Django 3.2 on 2023-08-03 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_auto_20230803_1436'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='player',
            name='Уникальная пара Партия - Игрок',
        ),
    ]
