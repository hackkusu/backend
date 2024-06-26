# Generated by Django 2.1.7 on 2024-03-13 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('camera_id', models.TextField(blank=True, null=True)),
                ('video_id', models.TextField(blank=True, null=True)),
                ('video_type', models.TextField(blank=True, null=True)),
                ('favorite', models.BooleanField(blank=True, null=True)),
                ('kind', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_date', models.DateTimeField()),
                ('video_date_local', models.DateTimeField()),
                ('detection_type', models.TextField(blank=True, null=True)),
                ('person_detected', models.BooleanField(blank=True, null=True)),
                ('source_url', models.TextField(blank=True, null=True)),
                ('bucket_name', models.CharField(blank=True, max_length=100, null=True)),
                ('filename', models.TextField()),
                ('filepath', models.TextField()),
                ('raw', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='profile_photo_url',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]
