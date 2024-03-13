# Create your models here.
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.test import TestCase
from django.conf import settings

# Create your tests here.
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, User as AuthUser
from django.db import models
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

# class User(AbstractUser):
#     """
#     Users within the Django authentication system are represented by this
#     model.
#
#     Username and password are required. Other fields are optional.
#     """
#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo_url = models.TextField(blank=True)
    class Meta:
        permissions = [
            ("can_create", "Can create a user"),
        ]

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_by = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Video(Model):
    id = models.AutoField(primary_key=True)
    camera_id = models.TextField(null=True, blank=True)
    video_id = models.TextField(null=True, blank=True)
    video_type = models.TextField(null=True, blank=True)
    favorite = models.BooleanField(null=True, blank=True)
    kind = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    video_date = models.DateTimeField()
    video_date_local = models.DateTimeField()
    detection_type = models.TextField(null=True, blank=True)
    person_detected = models.BooleanField(null=True, blank=True)
    source_url = models.TextField(null=True, blank=True)
    bucket_name = models.CharField(max_length=100, null=True, blank=True)
    filename = models.TextField()
    filepath = models.TextField()
    raw = models.TextField(null=True, blank=True)
    # sync = models.ForeignKey('SyncEvent', null=True, blank=True, related_name='videos', db_column='sync_id',
    #                          on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='users', db_column='user_id',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(null=False, default=timezone.now)
    updated = models.DateTimeField(null=False, auto_now=True)
