from django.http import HttpResponse
# from rest_framework_simplify.views import SimplifyView
# from twilio.twiml.messaging_response import Response
# Download the helper library from https://www.twilio.com/docs/python/install
from rest_framework.views import APIView
from twilio.rest import Client
import json

# from fireship.domain.models import Account

class TwilioHandler(APIView):
    # def __init__(self):
    #     super().__init__(None, supported_methods=['POST'])

    def post(self, request):
        account_sid = request.data.get('account_sid')
        auth_token = request.data.get('auth_token')
        workspace_sid = request.data.get('workspace_sid')
        workflow_sid = request.data.get('workflow_sid')
        attributes = request.data.get('attributes', {
            'type': 'support'
        })
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = account_sid
        auth_token = auth_token
        client = Client(account_sid, auth_token)

        task = client.taskrouter.workspaces(workspace_sid) \
            .tasks \
            .create(attributes=json.dumps(attributes), workflow_sid=workflow_sid)

        print(task.sid)

        # response = Response()
        # data = str(response)
        return HttpResponse(json.dumps(attributes), content_type='application/json')

    @staticmethod
    def scrub_phone_number(phone_number):
        if phone_number and len(phone_number) > 10:
            return phone_number[2:]
        return phone_number
