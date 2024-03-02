# from datetime import datetime
import datetime
import getpass
from django.core.management import BaseCommand

import pickle

import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
class Command(BaseCommand):
    help = 'One-time utility to authenticate with arlo'
    errors = []

    def add_arguments(self, parser):
        # parser.add_argument('-c', '--cookie', type=str, help='Define a cookie for requests')
        # parser.add_argument('-t', '--csrf', type=str, help='Define a csrf token')
        # parser.add_argument('storage_location',type=str)
        pass

    def handle(self, *args, **kwargs):
        FILENAME = 'gmail.credentials'
        PORT = 7788

        flow = InstalledAppFlow.from_client_secrets_file(
            'google_client_credentials.json',
            scopes=['https://www.googleapis.com/auth/gmail.readonly'])

        flow.redirect_uri = 'http://localhost:{}/'.format(PORT)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        credentials = flow.run_console(authorization_prompt_message='Please visit this URL: {}'.format(
                                                authorization_url))

        pickle.dump(credentials, open(FILENAME, 'wb'))
