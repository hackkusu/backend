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

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services.helper.service import HelperService

import environ
root = environ.Path(__file__) - 2
BASE_DIR = root()


logger = logging.getLogger(__name__)
User = get_user_model()

from django.http import JsonResponse
from google.cloud import storage
import os



@never_cache
@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_ip(request: HttpRequest, *args, **kwargs) -> HttpResponse:

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
