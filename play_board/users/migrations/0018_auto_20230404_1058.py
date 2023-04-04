# Generated by Django 3.2.18 on 2023-04-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20230403_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botconfig',
            name='radius',
        ),
        migrations.AddField(
            model_name='botconfig',
            name='loc_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Широта координаты центра поиска'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='loc_lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Долгота координаты центра поиска'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='max_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Макс.граница по широте'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='max_lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Макс.граница по широте'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='min_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Мин.граница по широте'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='min_lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Мин.граница по долготе'),
        ),
    ]
