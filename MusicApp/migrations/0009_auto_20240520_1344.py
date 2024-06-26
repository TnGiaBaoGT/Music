# Generated by Django 3.2 on 2024-05-20 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MusicApp', '0008_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='music_id_album',
            field=models.ManyToManyField(to='MusicApp.Music'),
        ),
        migrations.AddField(
            model_name='album',
            name='user_id_album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MusicApp.user'),
        ),
    ]
