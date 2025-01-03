# Generated by Django 3.2.8 on 2025-01-03 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0004_remove_guide_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='availability',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='travello.guide'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
