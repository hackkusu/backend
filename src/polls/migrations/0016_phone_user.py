# Generated by Django 2.1.7 on 2024-04-18 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_survey_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phones', to=settings.AUTH_USER_MODEL),
        ),
    ]
