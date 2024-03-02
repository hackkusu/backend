from django.db import models

# Create your models here.
from django.db.models import Model
from django.test import TestCase

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
