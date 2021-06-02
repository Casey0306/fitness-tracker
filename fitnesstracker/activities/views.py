from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import SaveUserActivitiesSerializer
from .models import Fitstat
import datetime
from django.utils import timezone


class SaveUserActivitiesView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = SaveUserActivitiesSerializer
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Activities saved successfully',
        }

        return Response(response, status=status_code)


class GetUserActivitiesView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            timedelta_string = request.GET["timedelta"]
            timedelta = 0
            result_running = datetime.timedelta(hours=0)
            result_walking = datetime.timedelta(hours=0)
            result_bicycle = datetime.timedelta(hours=0)
            result_calories = 0
            result_distance = 0
            if timedelta_string == "hour":
                timedelta = 1
            if timedelta_string == "day":
                timedelta = 24
            user = request.user
            if user.is_verified:
                time_low_border = \
                    timezone.now() - datetime.timedelta(hours=timedelta)
                result_queryset = \
                    Fitstat.objects.filter(
                        user=user,
                        start_time__gte=time_low_border,
                        stop_time__gte=time_low_border).all()
                for query in result_queryset:
                    result_calories = result_calories + query.calories
                    result_distance = result_distance + query.distance
                    temp_time = query.stop_time - query.start_time
                    action = query.type_of_activity.type_name
                    if action == "running":
                        result_running = result_running + temp_time
                    if action == "walking":
                        result_walking = result_walking + temp_time
                    if action == "bicycle":
                        result_bicycle = result_bicycle + temp_time
                status_code = status.HTTP_201_CREATED
                message = 'Summary statistic for a ' + timedelta_string
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'user email': user.email,
                    'message': message,
                    'running_stat': result_running,
                    'walking_stat': result_walking,
                    'bicycle_stat': result_bicycle,
                    'distance_summ': result_distance,
                    'calories_summ': result_calories,
                }

            else:
                raise NameError(
                    'Email does not verified')
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Error',
                'error': str(e)
                }
        return Response(response, status=status_code)
