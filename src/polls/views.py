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
from django.views import View
from django_ratelimit.decorators import ratelimit
from collections import Counter
from rest_framework.exceptions import PermissionDenied

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Survey, Phone, SurveyQuestion
from .serializers import UserSerializer, RegisterSerializer, SurveySerializer, PhoneSerializer, SurveyQuestionSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, QueryDict
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import humanize
from datetime import datetime

from .services.helper.service import HelperService

import environ

from .services.twilio.service import TwilioService

from rest_framework import viewsets, status

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncHour, TruncMinute
from datetime import timedelta

root = environ.Path(__file__) - 2
BASE_DIR = root()


logger = logging.getLogger(__name__)
User = get_user_model()

from django.http import JsonResponse
from google.cloud import storage
import os

from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.request_validator import RequestValidator
from .models import SMS, SurveyResponse
from .bll.qr.create_qr_bll import QRCodeBll

class QRCodeView(View):
    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number', '4352131896')  # or however you're passing the phone number
        start_code = request.GET.get('start_code', 'start')  # or however you're passing the phone number
        buffer = QRCodeBll.generate_and_return_bytes_buffer_qr_code(phone_number, start_code)
        # Return an HTTP response with the image and the correct MIME type
        return HttpResponse(buffer.getvalue(), content_type='image/png')

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def get_responses_over_time(request):
    # Determine the time spread of the latest responses
    latest_response = SurveyResponse.objects.latest('created').created
    earliest_response = SurveyResponse.objects.earliest('created').created
    time_spread = latest_response - earliest_response

    # Choose a truncation based on the time spread
    if time_spread <= timedelta(hours=1):
        trunc = TruncMinute
    elif time_spread <= timedelta(days=1):
        trunc = TruncHour
    else:
        trunc = TruncDay

    # Aggregate the count of positive and negative responses per time unit
    positive_responses = SurveyResponse.objects.filter(sentiment=SurveyResponse.POSITIVE).annotate(date=trunc('created')).values('date').annotate(count=Count('id')).order_by('date')
    negative_responses = SurveyResponse.objects.filter(sentiment=SurveyResponse.NEGATIVE).annotate(date=trunc('created')).values('date').annotate(count=Count('id')).order_by('date')

    # Ensure the data series end at the same time
    if positive_responses and negative_responses:
        last_positive_timestamp = positive_responses.last()['date']
        last_negative_timestamp = negative_responses.last()['date']
        latest_timestamp = max(last_positive_timestamp, last_negative_timestamp).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        latest_timestamp = latest_response.strftime("%Y-%m-%dT%H:%M:%S")

    pos_data = [{'x': resp['date'].strftime("%Y-%m-%dT%H:%M:%S"), 'y': resp['count']} for resp in positive_responses]
    neg_data = [{'x': resp['date'].strftime("%Y-%m-%dT%H:%M:%S"), 'y': resp['count']} for resp in negative_responses]

    # Append a zero value if the last timestamp of either sentiment doesn't match the latest timestamp
    if positive_responses and (positive_responses.last()['date'].strftime("%Y-%m-%dT%H:%M:%S") != latest_timestamp):
        pos_data.append({'x': latest_timestamp, 'y': 0})
    if negative_responses and (negative_responses.last()['date'].strftime("%Y-%m-%dT%H:%M:%S") != latest_timestamp):
        neg_data.append({'x': latest_timestamp, 'y': 0})

    # If there are no responses for either sentiment, append at least one data point to zero
    if not positive_responses:
        pos_data.append({'x': latest_timestamp, 'y': 0})
    if not negative_responses:
        neg_data.append({'x': latest_timestamp, 'y': 0})

    # React chart expects series data in a specific format
    series = [
        {
            'name': 'Positive Responses Over Time',
            'data': pos_data
        },
        {
            'name': 'Negative Responses Over Time',
            'data': neg_data
        }
    ]

    return JsonResponse({'series': series})


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def get_sentiment_overview(request):
    # Get total counts for each sentiment
    total_responses = SurveyResponse.objects.count()
    sentiment_counts = SurveyResponse.objects.values('sentiment').annotate(count=Count('id'))

    # Calculate the percentage of each sentiment
    sentiment_data = []
    for sentiment in sentiment_counts:
        if total_responses > 0:
            percentage = (sentiment['count'] / total_responses) * 100
        else:
            percentage = 0
        sentiment_data.append({
            'title': sentiment['sentiment'],
            'value': round(percentage, 2),  # round to two decimal places for neatness
            'color': 'success' if sentiment['sentiment'] == 'Positive' else 'danger' if sentiment['sentiment'] == 'Negative' else 'warning'
        })

    return JsonResponse({'progressbars': sentiment_data})

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def get_highlight_responses(request: HttpRequest) -> HttpResponse:
    # Fetch all responses
    all_responses = SurveyResponse.objects.order_by('-created').all()

    # Collect all aspects into a list
    all_aspects = []
    highlight_messages = []

    for response in all_responses:
        aspects_list = response.aspects.split(", ")
        all_aspects.extend(aspects_list)
        highlight_messages.append({
            'created': response.created.strftime("%Y-%m-%d %H:%M:%S"),  # Format date as needed
            'message': response.response_body,
            'sentiment': response.sentiment,
        })

    # Count occurrences of each aspect
    aspect_counts = Counter(all_aspects)

    # Find the top 5 aspects
    top_five_aspects = [aspect for aspect, count in aspect_counts.most_common(5)]

    # Simplify the message collection to just the most representative per sentiment
    sentiment_results = {}
    for sentiment in [SurveyResponse.POSITIVE, SurveyResponse.NEUTRAL, SurveyResponse.NEGATIVE]:
        sentiment_messages = [message for message in highlight_messages if message['sentiment'] == sentiment]
        if sentiment_messages:
            sentiment_results[sentiment] = sentiment_messages[0]  # Taking the most recent message
        else:
            sentiment_results[sentiment] = {
                'created': 'No date found',
                'message': 'No response found',
            }

    # Create a JSON response
    response_data = {
        "top_aspects": top_five_aspects,
        "messages": sentiment_results
    }

    return JsonResponse(response_data)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
def calculate_aspects(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    # Fetch all responses
    all_responses = list(SurveyResponse.objects.all().order_by('-created'))

    # Collect all aspects into a list
    all_aspects = []
    for response in all_responses:
        aspects_list = response.aspects.split(", ")
        all_aspects.extend(aspects_list)

    # Count occurrences of each aspect
    aspect_counts = Counter(all_aspects)

    # Find the top 5 aspects
    top_five_aspects = [aspect for aspect, count in aspect_counts.most_common(5)]

    # Find the most representative message for each sentiment
    sentiment_results = {}
    for sentiment in [SurveyResponse.POSITIVE, SurveyResponse.NEUTRAL, SurveyResponse.NEGATIVE]:
        max_count = 0
        best_response = None
        best_response_time = None
        for response in all_responses:
            if response.sentiment == sentiment:
                current_aspects = set(response.aspects.split(", "))
                top_aspect_count = sum(aspect in current_aspects for aspect in top_five_aspects)
                if top_aspect_count > max_count:
                    max_count = top_aspect_count
                    best_response = response.response_body
                    now = datetime.now(response.created.tzinfo)
                    best_response_time = humanize.naturaltime(now - response.created)

        sentiment_results[sentiment] = {
            'created': best_response_time,
            'message': best_response or "No response found",
            'sentiment': sentiment
        }

        # sentiment_results[sentiment] = {
        #     'created': response.created.strftime("%Y-%m-%d %H:%M:%S"),
        #     'message': best_response or "No response found",
        #     'sentiment': sentiment
        # }

    # Create a JSON response
    return JsonResponse({
        "top_aspects": top_five_aspects,
        "messages": sentiment_results
        # "messages": {
        #     "Positive": sentiment_results[SurveyResponse.POSITIVE]['message'],
        #     "Neutral": sentiment_results[SurveyResponse.NEUTRAL]['message'],
        #     "Negative": sentiment_results[SurveyResponse.NEGATIVE]['message']
        # }
    })

# todo: add twilio auth
@never_cache
@csrf_exempt
@require_http_methods(["POST"])
def sms_received(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    if request.META['HTTP_I_TWILIO_IDEMPOTENCY_TOKEN'] is None:
        raise Exception('bad request')

    data = QueryDict(request.body)

    try:
        TwilioService.process_inbound_message(data)
    except Exception as e:
        print(str(e))

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


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyQuestionSerializer
    # permission_classes = [TokenPresent]

    def get_queryset(self):
        # user_id = self.request.headers.get('X-User-ID')
        # return Survey.objects.all()
        return SurveyQuestion.objects.filter(survey__user_id=self.request.user.id)

    def perform_create(self, serializer):
        # user_id = self.request.user.id
        serializer.save()


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        request_user_id = self.request.user.id
        if instance.survey.user_id != request_user_id:
            return Response({"detail": "You do not have permission to update this entry."}, status=status.HTTP_403_FORBIDDEN)

        return super(SurveyQuestionViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response({'detail': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        request_user_id = self.request.user.id
        instance = self.get_object()
        if instance.survey.user_id != request_user_id:
            raise PermissionDenied({'detail': 'You do not have permission to delete this entry.'})

        response = super(SurveyQuestionViewSet, self).destroy(request, *args, **kwargs)
        return response
