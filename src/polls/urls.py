from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter
from django.conf.urls import include, url
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path

from .twilio.views import TwilioHandler
from . import views
from graphene_django.views import GraphQLView
from .schema import schema

__app_name__ = 'polls'

from .views import UserDetailAPI, RegisterUserAPIView, get_ip_anonymous, get_ip_login_required, get_ip_permission_required

urlpatterns = [
    # path('auth/', include('polls.authentication.urls')),
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("auth/get-details/", UserDetailAPI.as_view()),
    path('auth/register/', RegisterUserAPIView.as_view()),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),

    url(r'^get_ip_login_required$', get_ip_login_required),
    url(r'^get_ip_permission_required$', get_ip_permission_required),
    url(r'^get_ip_anonymous$', get_ip_anonymous),
    url(r'^createTask$', TwilioHandler.as_view()),
    url(r'^upload_video$', views.file_upload, name="upload_video"),
    url(r'^sms_received$', views.sms_received, name="sms_received"),
    # url(r'^v1/', include(router.urls)),

]
