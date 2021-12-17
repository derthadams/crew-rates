from django.apps import apps
from rest_framework import serializers


class RawRateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('rates', 'RawRateReport')
        fields = '__all__'


class JobTitleSerializer(serializers.Serializer): # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)


class ShowSerializer(serializers.Serializer):  # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)
