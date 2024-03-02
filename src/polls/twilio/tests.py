# import configurations
import os

# os.environ['DJANGO_SETTINGS_MODULE'] = 'fireship.settings'
# # setup the configuration local
# os.environ['DJANGO_CONFIGURATION'] = 'Local'
# configurations.setup()
import requests
from django.test import TestCase

# from rest_framework_signature.helpers import RestFrameworkSignatureTestClass
from rest_framework import status

from src.polls.twilio.views import TwilioHandler
from test.api_client import APIClient

from test.helpers import DataGenerator


class TwilioEndpointTests(TestCase):

    def test_url_parse(self):
        url = 'https://storage.cloud.google.com/00-zoot-video-results/00-zoot-video-queue/uploads/0bc27113-8222-4f48-b905-430f3acdf126_IMG_5930.mp4.001_dog_pct88_fr87.gif'
        result = url.split('/')[-1]
        self.assertEqual(result, '0bc27113-8222-4f48-b905-430f3acdf126_IMG_5930.mp4.001_dog_pct88_fr87.gif')

    def test_number_replacement(self):
        handler = TwilioHandler()
        number = handler.scrub_phone_number('+14356510466')
        number2 = handler.scrub_phone_number('1234567890')
        # assert
        self.assertEqual(number, '4356510466')
        self.assertEqual(number2, '1234567890')

    def test_number_replacement_none(self):
        handler = TwilioHandler()
        number = handler.scrub_phone_number(None)

        self.assertEqual(number, None)

    def test_number_replacement_not_enough_characters(self):
        handler = TwilioHandler()
        number = handler.scrub_phone_number('12345678')

        self.assertEqual(number, number)

    def test_post_no_data(self):
        # arrange
        body = {
        }

        url = '/api/createTask'
        # headers = self.get_headers(url, body=body)

        api_client = APIClient()

        # act
        # result = requests.post(url, body, json=True)
        result = api_client.post(url, body, content_type='application/json')

        # assert
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
