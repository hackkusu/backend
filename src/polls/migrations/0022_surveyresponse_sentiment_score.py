# Generated by Django 2.1.7 on 2024-04-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_surveyresponse_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='sentiment_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]