from django.apps import apps
from rest_framework import serializers


class RawRateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('rates', 'RawRateReport')
        fields = '__all__'


class SeasonSerializer(serializers.Serializer): # noqa
    uuid = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    season_title = serializers.CharField()
    union_status = serializers.CharField()
    genre = serializers.CharField()
    show_title = serializers.CharField()
    show_uuid = serializers.UUIDField()
    network_name = serializers.CharField()
    network_uuid = serializers.UUIDField()
    company_list = serializers.ListField(
        child=serializers.JSONField()
    )
    job_reports = serializers.ListField(
        child=serializers.JSONField()
    )


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


class FilterSearchSerializer(serializers.Serializer): # noqa
    value = serializers.UUIDField()
    label = serializers.CharField()
    type = serializers.CharField()