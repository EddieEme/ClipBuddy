# Generated by Django 4.2.17 on 2025-01-04 17:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clipapp', '0002_usertestimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestimonial',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
