# Generated by Django 2.1.7 on 2024-04-20 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20240420_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]