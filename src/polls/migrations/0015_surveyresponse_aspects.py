# Generated by Django 2.1.7 on 2024-04-17 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_surveyresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='aspects',
            field=models.TextField(default='none'),
        ),
    ]
