# Generated by Django 3.2.8 on 2025-01-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0002_auto_20250102_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guide',
            name='username',
            field=models.CharField(default=1, max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
