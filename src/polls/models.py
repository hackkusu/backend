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
# from storages.backends.gcloud import GoogleCloudStorage
# storage = GoogleCloudStorage()


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo_url = models.TextField(blank=True)
    class Meta:
        permissions = [
            ("can_create", "Can create a user"),
        ]

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    twilio_auth_token = models.CharField(max_length=34, null=False)
    twilio_account_sid = models.CharField(max_length=34, null=False)
    name = models.CharField(max_length=75, null=False)
    call_back_url = models.CharField(max_length=128, null=False)
    opt_in_confirmation_message = models.ForeignKey('Message', null=False, blank=False, default=1, related_name='accounts_using_opt_in_confirmation', on_delete=models.CASCADE)
    opt_out_confirmation_message = models.ForeignKey('Message', null=False, blank=False, default=2, related_name='accounts_using_opt_out_confirmation', on_delete=models.CASCADE)
    request_for_consent_message = models.ForeignKey('Message', null=False, blank=False, default=3, related_name='accounts_using_request_for_consent', on_delete=models.CASCADE)

    class Meta:
        db_table = 'account'

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    type = models.ForeignKey('MessageType', null=False, related_name='messages', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, null=False, blank=False)
    created = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        db_table = 'message'


class MessageType(models.Model):
    OPT_IN_CONFIRMATION_TYPE_ID = 1
    OPT_OUT_CONFIRMATION_TYPE_ID = 2
    REQUEST_FOR_CONSENT_TYPE_ID = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    created = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        db_table = 'message_type'


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15, null=False)
    label = models.CharField(max_length=200, null=True)
    twilio_sid = models.CharField(max_length=34, null=True, blank=True)
    account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)
    type = models.ForeignKey('PhoneType', null=False, blank=False, on_delete=models.CASCADE)
    send_from = models.ForeignKey('Phone', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'phone'


class PhoneType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, blank=False)

    class Meta:
        db_table = 'phone_type'


class SentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'sent_status'

class SMS(models.Model):
    id = models.AutoField(primary_key=True)
    to_number = models.CharField(max_length=15, null=False, blank=False)
    from_number = models.CharField(max_length=15, null=False, blank=False)
    message = models.CharField(max_length=1000, null=True, blank=True)
    twilio_sid = models.CharField(max_length=34, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)
    media_url = models.CharField(max_length=1000, null=True, blank=True)
    message_type = models.ForeignKey('MessageType', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms'

class SMSFile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    created = models.DateTimeField(default=timezone.now, null=False)
    processing = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'sms_file'


class SMSQueue(models.Model):
    id = models.AutoField(primary_key=True)
    processing = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    sms = models.ForeignKey('SMS', null=False, related_name='sms_queues', on_delete=models.CASCADE)
    opt_in_pending = models.BooleanField(default=False)
    send_date_time = models.DateTimeField(null=False)
    force_send = models.BooleanField(default=False)
    error_message = models.CharField(max_length=4000, null=True, blank=True)

    class ErrorMessages:
        INVALID_PHONE_TYPE_FOR_SENDING = 'Phone with type {0} cannot be sent from and no send_from configured for {1}'
        NO_PHONE_FOUND_FOR_FROM_NUMBER = 'No phone found with number: {0} to send from'

    class Meta:
        db_table = 'sms_queue'

    def send(self):
        import os
        environment = os.environ.get('DJANGO_CONFIGURATION')
        # If it's on Dev or Local, only send to numbers that are in the settings.TEXT_NUMBERS list
        not_production_environment = environment == 'Dev' or environment == 'Local'
        if not_production_environment and self.sms.to_number not in settings.TEXT_NUMBERS:
            return None
        else:
            return self.send_twilio()

    def send_twilio(self):
        # send texts logic goes here
        pass

class SMSOptIn(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15, null=False)
    created = models.DateTimeField(null=False, default=timezone.now)
    account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms_opt_in'

class SMSOptOut(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15, null=False)
    created = models.DateTimeField(null=False, default=timezone.now)
    account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms_opt_out'

class SMSReceived(models.Model):
    id = models.AutoField(primary_key=True)
    time_received = models.DateTimeField(default=timezone.now, null=True)
    sms = models.ForeignKey('SMS', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms_received'

    def is_opted_in(self):
        return SMSOptIn.objects.filter(
            number=self.sms.from_number, account_id=self.sms.account_id).exists()

    def is_opted_out(self):
        return SMSOptOut.objects.filter(
            number=self.sms.from_number, account_id=self.sms.account_id).exists()


class SMSSent(models.Model):
    id = models.AutoField(primary_key=True)
    time_sent = models.DateTimeField(default=timezone.now, null=True, blank=True)
    sms = models.ForeignKey('SMS', null=False, related_name='sms_sent', on_delete=models.CASCADE)
    sent_status = models.ForeignKey('SentStatus', null=False, on_delete=models.CASCADE)
    class Meta:
        db_table = 'sms_sent'

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=80, null=True)
#     password = models.CharField(max_length=128)
#     first_name = models.CharField(max_length=100, null=False, blank=False)
#     last_name = models.CharField(max_length=100, null=False, blank=False)
#     active = models.BooleanField(null=False, default=True)
#     created = models.DateTimeField(null=False, default=timezone.now)
#     salt = models.CharField(max_length=50, null=True)
#     password_reset_token = models.CharField(max_length=50, null=True)
#     password_reset_token_created = models.DateTimeField(null=True)
#     password_reset_ip = models.GenericIPAddressField(null=True)
#     failed_login_attempts = models.IntegerField(null=True, default=0)
#     last_failed_login = models.DateTimeField(null=True)
#
#     class Meta:
#         db_table = 'user'
#
#     # authentication requires an is_active field
#     @property
#     def is_active(self):
#         return self.active











# other stuff

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

