# Generated by Django 3.2.8 on 2025-01-03 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0006_remove_booking_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='message',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
