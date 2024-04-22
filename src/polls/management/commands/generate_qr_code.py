# from datetime import datetime
import datetime
import getpass
from django.core.management import BaseCommand
from ...bll.qr.create_qr_bll import QRCodeBll

import pickle

import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

# stackvidhya.com/list-contents-of-s3-bucket-using-boto3-python/
# https://aws.plainenglish.io/how-to-detect-objects-using-python-and-aws-rekognition-e8223a0fca51
# https://www.pluralsight.com/guides/computer-vision-with-amazon-rekognition
# from src.polls.services.rekognition.service import RekognitionService


class Command(BaseCommand):
    help = 'One-time utility to detect_labels with aws rekognition using s3'
    errors = []

    def add_arguments(self, parser):
        # parser.add_argument('-c', '--cookie', type=str, help='Define a cookie for requests')
        # parser.add_argument('-t', '--csrf', type=str, help='Define a csrf token')
        # parser.add_argument('storage_location',type=str)
        pass

    def handle(self, *args, **kwargs):
        try:
            QRCodeBll.generate_and_save_qr_code('4352131896', 'yea')
        except Exception as err:
            print(str(err))
            exit(1)
