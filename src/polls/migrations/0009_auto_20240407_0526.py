# Generated by Django 2.1.7 on 2024-04-07 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20240407_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sms',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Account'),
        ),
    ]
