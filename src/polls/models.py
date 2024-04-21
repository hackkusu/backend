# Create your models here.
import uuid
import pusher
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

from django.db.models.signals import post_save
from django.dispatch import receiver

class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False)
    icon = models.CharField(max_length=250, null=False)
    level = models.IntegerField(null=False, default=1)
    required_prior_achievement = models.ForeignKey('Achievement', related_name='prior_achievements', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, null=False)
    active = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = 'achievement'

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    twilio_auth_token = models.CharField(max_length=34, null=False)
    twilio_account_sid = models.CharField(max_length=34, null=False)
    name = models.CharField(max_length=75, null=False)
    call_back_url = models.CharField(max_length=128, null=True, blank=True)
    # opt_in_confirmation_message = models.ForeignKey('Message', null=False, blank=False, default=1, related_name='accounts_using_opt_in_confirmation', on_delete=models.CASCADE)
    # opt_out_confirmation_message = models.ForeignKey('Message', null=False, blank=False, default=2, related_name='accounts_using_opt_out_confirmation', on_delete=models.CASCADE)
    # request_for_consent_message = models.ForeignKey('Message', null=False, blank=False, default=3, related_name='accounts_using_request_for_consent', on_delete=models.CASCADE)

    class Meta:
        db_table = 'account'

# class Message(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=64, null=False, blank=False)
#     type = models.ForeignKey('MessageType', null=False, related_name='messages', on_delete=models.CASCADE)
#     text = models.CharField(max_length=1000, null=False, blank=False)
#     created = models.DateTimeField(null=False, default=timezone.now)
#
#     class Meta:
#         db_table = 'message'
#
#
# class MessageType(models.Model):
#     OPT_IN_CONFIRMATION_TYPE_ID = 1
#     OPT_OUT_CONFIRMATION_TYPE_ID = 2
#     REQUEST_FOR_CONSENT_TYPE_ID = 3
#
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=64, null=False, blank=False)
#     created = models.DateTimeField(null=False, default=timezone.now)
#
#     class Meta:
#         db_table = 'message_type'


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15, null=False)
    label = models.CharField(max_length=200, null=True)
    twilio_sid = models.CharField(max_length=34, null=True, blank=True)
    account = models.ForeignKey('Account', null=True, blank=True, related_name='phones', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='phones', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'phone'

# class SentStatus(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20, null=False, blank=False)
#
#     class Meta:
#         db_table = 'sent_status'

class SMS(models.Model):
    # INCOMING = 'Incoming'
    # OUTGOING = 'Outgoing'
    # DIRECTION_CHOICES = ((INCOMING, 'Incoming'), (OUTGOING, 'Outgoing'))

    id = models.AutoField(primary_key=True)
    to_number = models.CharField(max_length=15, null=False, blank=False)
    from_number = models.CharField(max_length=15, null=False, blank=False)
    message = models.CharField(max_length=1000, null=True, blank=True)
    twilio_sid = models.CharField(max_length=34, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    account = models.ForeignKey('Account', null=True, blank=True, on_delete=models.CASCADE) # todo: here
    media_url = models.CharField(max_length=1000, null=True, blank=True)
    # message_type = models.ForeignKey('MessageType', null=True, blank=True, on_delete=models.CASCADE)
    # direction = models.CharField(choices=DIRECTION_CHOICES, max_length=75, null=True, blank=True) # <-- todo here

    class Meta:
        db_table = 'sms'


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='ID')
    phone_number = models.CharField(max_length=15, null=False, db_column='PhoneNumber')
    survery = models.ForeignKey(
        'Survey',
        null=False,
        related_name='conversations',
        on_delete=models.CASCADE
    )
    unread = models.BooleanField(null=False, default=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    # opted_out = models.BooleanField(null=False, default=False)
    # opted_in = models.BooleanField(null=False, default=False)
    last_sms = models.ForeignKey(
        'Sms',
        null=True,
        blank=True,
        related_name='conversations',
        on_delete=models.CASCADE
    )
    last_survey_question = models.ForeignKey(
        'SurveyQuestion',
        null=True,
        blank=True,
        related_name='conversations',
        on_delete=models.CASCADE
    )
    closed = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = 'conversation'

    @property
    def default_from_number(self):
        return None

class SmsConversation(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='ID')
    sms = models.ForeignKey(
        'Sms',
        null=False,
        related_name='sms_conversations',
        on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        'Conversation',
        null=False,
        related_name='sms_conversations',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(default=timezone.now, null=False)
    class Meta:
        db_table = 'sms_conversation'
        unique_together = ('sms', 'conversation')

# class SMSFile(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=150, null=False)
#     created = models.DateTimeField(default=timezone.now, null=False)
#     processing = models.BooleanField(default=False, null=False)
#
#     class Meta:
#         db_table = 'sms_file'


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

# class SMSOptIn(models.Model):
#     id = models.AutoField(primary_key=True)
#     number = models.CharField(max_length=15, null=False)
#     created = models.DateTimeField(null=False, default=timezone.now)
#     account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'sms_opt_in'
#
# class SMSOptOut(models.Model):
#     id = models.AutoField(primary_key=True)
#     number = models.CharField(max_length=15, null=False)
#     created = models.DateTimeField(null=False, default=timezone.now)
#     account = models.ForeignKey('Account', null=False, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'sms_opt_out'

class SMSReceived(models.Model):
    id = models.AutoField(primary_key=True)
    time_received = models.DateTimeField(default=timezone.now, null=True)
    sms = models.ForeignKey('SMS', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms_received'

    # def is_opted_in(self):
    #     return SMSOptIn.objects.filter(
    #         number=self.sms.from_number, account_id=self.sms.account_id).exists()
    #
    # def is_opted_out(self):
    #     return SMSOptOut.objects.filter(
    #         number=self.sms.from_number, account_id=self.sms.account_id).exists()


class SMSSent(models.Model):
    id = models.AutoField(primary_key=True)
    time_sent = models.DateTimeField(default=timezone.now, null=True, blank=True)
    sms = models.ForeignKey('SMS', null=False, related_name='sms_sent', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sms_sent'

def generate_partial_uuid():
    return str(uuid.uuid4())[:5]

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    start_code = models.CharField(max_length=10, null=False, blank=False, default=generate_partial_uuid)
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    phone = models.ForeignKey('Phone', related_name='surveys', on_delete=models.CASCADE, null=True, blank=True) # todo: here
    user = models.ForeignKey('User', related_name='surveys', on_delete=models.CASCADE, null=True, blank=True)
    qr_code_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'survey'
        unique_together = ('start_code', 'phone')


class SurveyQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    question = models.CharField(null=True, blank=True, max_length=160)
    sort_order = models.IntegerField(default=0)
    survey = models.ForeignKey('Survey', related_name='survey_questions', on_delete=models.CASCADE)
    class Meta:
        db_table = 'survey_question'

class SurveyResponse(models.Model):
    POSITIVE = 'Positive'
    NEUTRAL = 'Neutral'
    NEGATIVE = 'Negative'
    SENTIMENT_CHOICES = ((POSITIVE, 'Positive'), (NEUTRAL, 'Neutral'), (NEGATIVE, 'Negative'))

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    response_body = models.TextField(null=False)
    aspects = models.TextField(null=False, default='none')
    sentiment = models.CharField(choices=SENTIMENT_CHOICES, max_length=15)
    survey = models.ForeignKey('Survey', related_name='survey_responses', on_delete=models.CASCADE, null=True, blank=True)
    survey_question = models.ForeignKey('SurveyQuestion', related_name='survey_responses', on_delete=models.CASCADE)
    sentiment_score = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=5)

    class Meta:
        db_table = 'survey_response'

@receiver(post_save, sender=SurveyResponse)
def broadcast_update(sender, instance, created, **kwargs):
    if created:
        pusher_client = pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )

        pusher_client.trigger('survey-response-channel', 'new-response', {
            'message': 'A new response was added.'
            # You can send more data as needed
        })

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


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo_url = models.TextField(blank=True)

    class Meta:
        db_table = 'user'
        permissions = [
            ("can_create", "Can create a user"),
        ]

class UserAchievement(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.IntegerField(null=True, blank=True, default=1)
    percent_complete = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey('User', related_name='user_achievements', null=False, on_delete=models.CASCADE)
    achievement = models.ForeignKey('Achievement', related_name='user_achievements', null=False, on_delete=models.CASCADE)
    completed_on = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        db_table = 'user_achievement'
        unique_together = ('user', 'achievement')


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='user_profiles', null=False, on_delete=models.CASCADE, unique=True)
    dark_mode = models.BooleanField(null=True, blank=True, default=True)
    profile_photo_url = models.TextField(blank=True, null=True)




# other stuff

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_by = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'recipe'

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

    class Meta:
        db_table = 'video'
