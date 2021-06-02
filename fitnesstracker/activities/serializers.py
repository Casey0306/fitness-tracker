from rest_framework import serializers
from .models import Fitstat, Acttype


class SaveUserActivitiesSerializer(serializers.ModelSerializer):

    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    stop_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    type_of_activity = serializers.CharField(max_length=255)
    distance = serializers.IntegerField()
    calories = serializers.IntegerField()

    class Meta:
        model = Fitstat
        fields = ('start_time', 'stop_time',
                  'type_of_activity', 'distance', 'calories')

    def validate(self, attrs):
        tp_attrs = attrs.get('type_of_activity', None)
        tp = Acttype.objects.filter(type_name=tp_attrs).first()
        if tp is None:
            raise serializers.ValidationError(
                'Type of activities does not exists')
        return attrs

    def create(self, validated_data):
        user = validated_data.get('owner', None)
        tpoa_val = validated_data.get('type_of_activity', None)
        tpoa = Acttype.objects.filter(type_name=tpoa_val).first()
        if user.is_verified is True:
            statistic = Fitstat.objects.create(user=user,
                                               start_time=validated_data.get(
                                                   'start_time', None),
                                               stop_time=validated_data.get(
                                                   'stop_time', None),
                                               type_of_activity=tpoa,
                                               distance=validated_data.get(
                                                   'distance', None),
                                               calories=validated_data.get(
                                                   'calories', None))

        else:
            raise serializers.ValidationError('Email does not verified')

        return statistic
