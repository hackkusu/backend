import datetime
import json
import logging
import os
import pickle
import time
import platform
import socket
import uuid
import pytz
import requests
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from rest_framework.exceptions import PermissionDenied

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Survey, Phone
from .serializers import UserSerializer, RegisterSerializer, SurveySerializer, PhoneSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, QueryDict
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services.helper.service import HelperService

import environ

from .services.twilio.service import TwilioService

from rest_framework import viewsets, status

root = environ.Path(__file__) - 2
BASE_DIR = root()


logger = logging.getLogger(__name__)
User = get_user_model()

from django.http import JsonResponse
from google.cloud import storage
import os

from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.request_validator import RequestValidator



# todo: add twilio auth
@never_cache
@csrf_exempt
@require_http_methods(["POST"])
def sms_received(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    if request.META['HTTP_I_TWILIO_IDEMPOTENCY_TOKEN'] is None:
        raise Exception('bad request')

    data = QueryDict(request.body)

    TwilioService.process_inbound_message(data)

    # response = MessagingResponse()
    # response.message('This is message 1 of 2.')

    response = Response()
    data = str(response)

    return HttpResponse(data, content_type='text/xml')

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def get_ip_anonymous(request: HttpRequest, *args, **kwargs) -> HttpResponse:

    print(HelperService().get_ip_address(request))
    return HttpResponse(HelperService.get_ip_address(request), status=200)

@login_required
@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def get_ip_login_required(request: HttpRequest, *args, **kwargs) -> HttpResponse:

    print(HelperService().get_ip_address(request))
    return HttpResponse(HelperService.get_ip_address(request), status=200)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@permission_required('polls.can_create', raise_exception=True)
def get_ip_permission_required(request: HttpRequest, *args, **kwargs) -> HttpResponse:

    print(HelperService().get_ip_address(request))
    return HttpResponse(HelperService.get_ip_address(request), status=200)

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


@csrf_exempt
@permission_required('polls.can_create', raise_exception=True)
@ratelimit(key='user_or_ip', rate='2/30s')
@ratelimit(key='user_or_ip', rate='25/10m')
@ratelimit(key='user_or_ip', rate='2900/d')
@require_http_methods(["POST"])
def file_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        created = datetime.datetime.utcnow()
        bucket_name = '00-zoot-video-queue'
        est = pytz.timezone('America/Denver')
        my_uuid = str(uuid.uuid4())
        filename = file.name
        # filename = my_uuid + '_' + file.name
        filepath = 'uploads/' + filename
        # filepath = 'uploads/' + my_uuid + '_' + filename
        external_id = filename
        path1 = created.astimezone(est).strftime("%Y/%m/%d")
        url = 'https://storage.cloud.google.com/00-zoot-video-queue/' + filepath

        # sync_event = SyncEvent(external_id=external_id, pending=True, source=SyncEvent.UPLOAD)
        #
        # try:
        #     sync_event.save()
        # except Exception as err:
        #     print('{} Error - {} - {}'.format(SyncEvent.UPLOAD, str(external_id), str(err)))
        #     error_model = SyncError(external_id=sync_event.external_id, error_msg=str(err),
        #                             type=SyncError.PARSE_ERROR_TYPE)
        #     error_model.save()
        #     sync_event.pending = False
        #     sync_event.success = False
        #     sync_event.save()
        #     return JsonResponse({'status': 'error', 'message': str(err)})
        #
        # try:
        #     # Google Cloud Storage setup
        #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, 'security-videos-346723-1ef9efdefc15.json')
        #     client = storage.Client()
        #     bucket = client.get_bucket('00-zoot-video-queue')
        #
        #     # Upload the file
        #     blob = bucket.blob('uploads/' + file.name)
        #     # blob = bucket.blob('uploads/' + my_uuid + '_' + file.name)
        #     # blob = bucket.blob('uploads/' + request.user.username + '/' + str(uuid.uuid4()) + '_' + file.name)
        #     blob.upload_from_file(file)
        # except Exception as err:
        #     print('{} Error - {} - {}'.format(SyncEvent.UPLOAD, str(external_id), str(err)))
        #     error_model = SyncError(external_id=sync_event.external_id, error_msg=str(err),
        #                             type=SyncError.UPLOAD_ERROR)
        #     error_model.save()
        #     sync_event.pending = False
        #     sync_event.success = False
        #     sync_event.save()
        #     return JsonResponse({'status': 'error', 'message': str(err)})
        #
        #
        # video_model = Video(video_date=created,
        #                     video_date_local=created.astimezone(est),
        #                     video_id=external_id,
        #                     # video_type=video_type,
        #                     # kind=kind,
        #                     source_url=url,
        #                     bucket_name=bucket_name,
        #                     filepath=filepath,
        #                     filename=filename,
        #                     # raw=json.dumps(video, default=str, indent=4, sort_keys=True),
        #                     sync=sync_event,
        #                     user_id=request.user.id
        #                     )
        #
        # video_model.save()

        return JsonResponse({'status': 'success', 'message': 'File uploaded successfully', 'externalId': external_id, 'syncEventId': sync_event.id })
    else:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'})

class PhoneViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneSerializer
    # permission_classes = [TokenPresent]

    def get_queryset(self):
        user_id = self.request.user.id
        return Phone.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(user_id=user_id)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        request_user_id = self.request.user.id
        if instance.user_id != request_user_id:
            return Response({"detail": "You do not have permission to update this entry."}, status=status.HTTP_403_FORBIDDEN)

        return super(PhoneViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response({'detail': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        request_user_id = self.request.user.id
        instance = self.get_object()
        if instance.user_id != request_user_id:
            raise PermissionDenied({'detail': 'You do not have permission to delete this entry.'})

        response = super(PhoneViewSet, self).destroy(request, *args, **kwargs)
        return response

class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    # permission_classes = [TokenPresent]

    def get_queryset(self):
        # user_id = self.request.headers.get('X-User-ID')
        # return Survey.objects.all()
        return Survey.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(user_id=user_id)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        request_user_id = self.request.user.id
        if instance.user_id != request_user_id:
            return Response({"detail": "You do not have permission to update this entry."}, status=status.HTTP_403_FORBIDDEN)

        return super(SurveyViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response({'detail': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        request_user_id = self.request.user.id
        instance = self.get_object()
        if instance.user_id != request_user_id:
            raise PermissionDenied({'detail': 'You do not have permission to delete this entry.'})

        response = super(SurveyViewSet, self).destroy(request, *args, **kwargs)
        return response
