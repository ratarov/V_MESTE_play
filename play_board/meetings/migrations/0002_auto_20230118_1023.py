# Generated by Django 3.2 on 2023-01-18 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_place'),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetings', to='users.place'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('готовится', 'готовится'), ('завершена', 'завершена'), ('отменена', 'отменена')], max_length=30),
        ),
        migrations.DeleteModel(
            name='Place',
        ),
    ]
