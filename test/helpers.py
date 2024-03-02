import datetime
import uuid

from django.utils import timezone
# from fireship.domain.models import Account


class DataGenerator:
    def __init__(self):
        pass
    # @staticmethod
    # def set_up_account(twilio_auth_token=None, twilio_account_sid=None, name=None):
    #     account = Account(twilio_auth_token=str(uuid.uuid4())[:15], twilio_account_sid=str(uuid.uuid4())[:34],
    #                       name=str(uuid.uuid4())[:35], call_back_url=str(uuid.uuid4())[:34])
    #     if twilio_auth_token:
    #         account.twilio_auth_token = twilio_auth_token
    #     if twilio_account_sid:
    #         account.twilio_account_sid = twilio_account_sid
    #     if name:
    #         account.name = name
    #     account.save()
    #     return account

class TwilioTestClient:

    def __init__(self, sid, token):
        self.sid = sid
        self.token = token
        self.messages = TwillioTestClientMessages()

class TwillioTestClientMessages:
    created = []

    def create(self, to, from_, body):
        self.created.append({
            'to': to,
            'from_': from_,
            'body': body
        })


def test_logger():
    import logging
    logger = logging.getLogger(__name__)
    logger.info('Logz.io Test Message')


def test_request_logger():
    import logging
    logger = logging.getLogger('django.request')
    extra_loggin = {
        'rq_query_params': '?ask=1&id=515',
        'rq_data': {'key1': 1, 'key2': 2},
        'rq_method': 'POST',
        'rq_path': '/lefevre/is/awesome',
        'rs_status_code': 400
    }
    logger.info('Logz.io Test Request Log', extra=extra_loggin)
