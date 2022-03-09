import json

from django.apps import apps
from rest_framework import serializers


class RawRateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('rates', 'RawRateReport')
        fields = '__all__'


class RateReportSerializer(serializers.Serializer): # noqa
    uuid = serializers.UUIDField()
    percent_increase = serializers.IntegerField()
    guarantee = serializers.IntegerField()
    daily = serializers.DecimalField(
        decimal_places=0,
        max_digits=8
    )
    hourly = serializers.DecimalField(
        decimal_places=2,
        max_digits=7
    )
    union_status = serializers.CharField()
    show_title = serializers.CharField()
    season_number = serializers.IntegerField()
    genre = serializers.CharField()
    job_title_name = serializers.CharField()
    network = serializers.CharField()
    season__start_date = serializers.DateField()
    season__end_date = serializers.DateField()
    companies = serializers.ListField(
        child=serializers.JSONField()
    )


class JSONLoadsField(serializers.Field): # noqa

    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        return json.loads(data)


class SeasonSerializer(serializers.Serializer): # noqa
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    season_title = serializers.CharField()
    union_status = serializers.CharField()
    genre = serializers.CharField()
    show_title = serializers.CharField()
    show_uuid = serializers.UUIDField()
    network_name = serializers.CharField()
    network_uuid = serializers.UUIDField()
    company_list = JSONLoadsField()
    job_reports = JSONLoadsField()


class JobTitleSerializer(serializers.Serializer): # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)


class ShowSerializer(serializers.Serializer):  # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)


class CompanySerializer(serializers.Serializer):  # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)

class NetworkSerializer(serializers.Serializer):  # noqa
    value = serializers.UUIDField()
    label = serializers.CharField(max_length=128)