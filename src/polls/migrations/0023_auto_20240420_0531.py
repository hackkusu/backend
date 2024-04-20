# Generated by Django 2.1.7 on 2024-04-20 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_surveyresponse_sentiment_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='sentiment_score',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True),
        ),
    ]