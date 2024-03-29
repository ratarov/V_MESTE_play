# Generated by Django 3.2.18 on 2023-07-12 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ('-date',), 'verbose_name': 'Игрок', 'verbose_name_plural': 'Игроки'},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('-winner', 'name'), 'verbose_name': 'Игрок', 'verbose_name_plural': 'Игроки'},
        ),
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('draft', 'черновик'), ('ignore', 'пропуск'), ('ok', 'ок')], default='draft', max_length=10),
        ),
        migrations.AlterField(
            model_name='match',
            name='ignore',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='matches.match'),
        ),
    ]
