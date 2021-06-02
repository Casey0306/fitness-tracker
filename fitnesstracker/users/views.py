from .renderers import UserRenderer
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,\
    RetrieveAPIView, CreateAPIView
from .serializers import RegisterSerializer, EmailVerificationSerializer,\
    GetTokenSerializer, RepeatedSentEmailSerializer
from django.urls import reverse
from .models import User
from .utils import Util
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from django.conf import settings
import datetime


class RegisterView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        dt = datetime.datetime.now() + datetime.timedelta(seconds=3600)
        token_enc = jwt.encode({
            'id': user.id,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        token = token_enc.decode('utf-8')
        update_last_login(None, user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi ' + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class RepeatedSentEmailVerifyView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RepeatedSentEmailSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        dt = datetime.datetime.now() + datetime.timedelta(seconds=3600)
        token_enc = jwt.encode({
            'id': user.id,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        token = token_enc.decode('utf-8')
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink +\
                 "?token=" + str(token)
        email_body = 'Hi ' + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):

    permission_classes = (AllowAny,)
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Token is generated succesfully',
            'token': serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
