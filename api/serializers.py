from django.apps import apps
from rest_framework import pagination, serializers


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


class SeasonPagination(pagination.CursorPagination):
    ordering = ['-start_date', 'uuid']
    page_size = 5


class HistogramSerializer(serializers.Serializer): # noqa
    bins = serializers.JSONField()
    bin_size = serializers.IntegerField()
    med = serializers.FloatField()


class SummarySerializer(serializers.Serializer): # noqa
    histogram = HistogramSerializer()
    statistics = serializers.JSONField()
    rate_count = serializers.IntegerField()
    heading = serializers.CharField()
    start_date = serializers.DateField()
    union_title = serializers.CharField()
    genre_title = serializers.CharField()


# class FeedSerializer(serializers.Serializer): # noqa
#     reports = SeasonSerializer(many=True)
#     summary = SummarySerializer()


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