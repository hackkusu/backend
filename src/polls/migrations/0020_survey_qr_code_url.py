# Generated by Django 2.1.7 on 2024-04-20 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_auto_20240420_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='qr_code_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]