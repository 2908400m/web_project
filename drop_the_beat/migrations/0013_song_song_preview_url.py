# Generated by Django 2.2.28 on 2025-03-26 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drop_the_beat', '0012_auto_20250321_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_preview_url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
