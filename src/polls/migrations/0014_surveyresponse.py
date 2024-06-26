# Generated by Django 2.1.7 on 2024-04-08 21:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20240407_0554'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('response_body', models.TextField()),
                ('sentiment', models.CharField(choices=[('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')], max_length=15)),
                ('survey_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_responses', to='polls.SurveyQuestion')),
            ],
            options={
                'db_table': 'survey_response',
            },
        ),
    ]
