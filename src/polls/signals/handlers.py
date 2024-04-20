import binascii
import datetime
import os
import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

from ..bll.qr.create_qr_bll import QRCodeBll

from ..models import Survey

@receiver(pre_save, sender=Survey)
def update_dependent_field(sender, instance, **kwargs):
    if not instance.qr_code_url:
        url = QRCodeBll.generate_qr_code(instance.phone.number)
        instance.qr_code_url = url
