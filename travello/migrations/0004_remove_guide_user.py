# Generated by Django 3.2.8 on 2025-01-02 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0003_auto_20250102_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='user',
        ),
    ]
