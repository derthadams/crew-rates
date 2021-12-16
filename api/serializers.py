from django.apps import apps
from rest_framework import serializers


class RawRateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('rates', 'RawRateReport')
        fields = '__all__'
