from datetime import date, timedelta
import requests

from django.apps import apps
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Count, Exists, F, IntegerField, Min, Max, OuterRef, Value
from django.db.models.functions import Cast, Floor, JSONObject
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rates.models import Company, JobTitle, Network, RateReport, Season, Show # noqa

from .api_config import *
from .postgres import ArraySubquery, Median
from .serializers import RawRateReportSerializer, JobTitleSerializer, \
    ShowSerializer, CompanySerializer, NetworkSerializer, SeasonSerializer, FilterSearchSerializer,\
    SummarySerializer, SeasonPagination

from rates.admin import _approve_raw_rate_report # noqa


class LocationAutocompleteAPIView(APIView):

    def get(self, request):
        params = {
            "input": self.request.GET.get('q'),
            "sessiontoken": self.request.GET.get('sessiontoken'),
            "key": APIKey,
            "language": "en-US",
            "type": "(regions)"
        }
        response = requests.get(SEARCH_URL, params=params)
        return Response(response.json(), status=status.HTTP_200_OK)


class LocationDetailsAPIView(APIView):

    def get(self, request):
        params = {
            "place_id": self.request.GET.get('q'),
            "sessiontoken": self.request.GET.get('sessiontoken'),
            "key": APIKey,
            "fields": "formatted_address,address_components,geometry",
            "language": "en-US"
        }
        response = requests.get(DETAILS_URL, params=params)
        return Response(response.json(), status=status.HTTP_200_OK)


class JobTitlesAPIView(APIView):

    def get(self, request):  # noqa
        job_title = apps.get_model('rates', 'JobTitle')
        results = list(job_title.objects.filter(
            title__icontains=request.GET.get('q')
        ).annotate(value=F('uuid'), label=F('title')).values('value', 'label'))
        data = JobTitleSerializer(results, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ShowsAPIView(APIView):

    def get(self, request):
        show = apps.get_model('rates', 'Show')
        results = list(
            show.objects.filter(
                title__icontains=self.request.GET.get('q')
            )
            .annotate(value=F('uuid'), label=F('title'))
            .values('value', 'label'))
        data = ShowSerializer(results, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class CompaniesAPIView(APIView):

    def get(self, request):
        company = apps.get_model('rates', 'Company')
        results = list(
            company.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(value=F('uuid'), label=F('name'))
            .values('value', 'label'))
        data = CompanySerializer(results, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class NetworksAPIView(APIView):

    def get(self, request):
        network = apps.get_model('rates', 'Network')
        results = list(
            network.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(value=F('uuid'), label=F('name'))
            .values('value', 'label'))
        data = NetworkSerializer(results, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class AddRate(APIView):
    uuid_null = '00000000-0000-0000-0000-000000000000'

    def post(self, request):  # noqa
        data = request.data
        data['user'] = request.user.id
        serializer = RawRateReportSerializer(data=data)
        if serializer.is_valid():
            job_title_matches = []
            show_matches = []
            company_matches = []
            network_matches = []
            user_created_values = False

            if serializer.validated_data['job_title'] == self.uuid_null:
                user_created_values = True
                job_title_matches = apps.get_model('rates', 'JobTitle').objects.annotate(
                    similarity=TrigramSimilarity('title',
                                                 serializer.validated_data['job_title_name']),
                ).filter(similarity__gt=0.3).order_by('-similarity')

            if serializer.validated_data['show'] == self.uuid_null:
                user_created_values = True
                show_matches = apps.get_model('rates', 'Show').objects.annotate(
                    similarity=TrigramSimilarity('title', serializer.validated_data['show_title']),
                ).filter(similarity__gt=0.3).order_by('-similarity')

            companies = serializer.validated_data['companies']
            for company in companies:
                if company['uuid'] == self.uuid_null:
                    user_created_values = True
                    query_results = list(apps.get_model('rates', 'Company').objects.annotate(
                        similarity=TrigramSimilarity('name', company['name']),
                    ).filter(similarity__gt=0.3).order_by('-similarity'))
                    company_matches.extend(query_results)

            if serializer.validated_data['network'] == self.uuid_null:
                user_created_values = True
                network_matches = apps.get_model('rates', 'Network').objects.annotate(
                    similarity=TrigramSimilarity('name', serializer.validated_data['network_name']),
                ).filter(similarity__gt=0.3).order_by('-similarity')

            raw_report = serializer.save(
                job_title_matches=job_title_matches,
                show_matches=show_matches,
                company_matches=company_matches,
                network_matches=network_matches,
                user_created_values=user_created_values
            )

            if not user_created_values and settings.AUTO_APPROVE_RATE_REPORTS:
                _approve_raw_rate_report(raw_report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeasonListAPIView(APIView, SeasonPagination):

    def get(self, request, format=None): # noqa
        date_range = request.GET.get('date_range', '')
        if date_range.isnumeric():
            date_range = int(date_range)
        union_select = request.GET.get('union_select', '')
        genre_select = request.GET.get('genre_select', '')
        filter_uuid = request.GET.get('filter_uuid', '')
        filter_type = request.GET.get('filter_type', '')

        results = Season.objects.all()

        if date_range:
            duration = timedelta(days=(30 * date_range))
            date_limit = date.today() - duration
            results = results.filter(start_date__gte=date_limit)

        if union_select != 'AA':
            results = results.filter(union__exact=union_select)

        if genre_select != 'AA':
            results = results.filter(genre__exact=genre_select)

        if filter_uuid and filter_type:
            if filter_type == "Show":
                results = results.filter(show__uuid=filter_uuid)
            elif filter_type == "Network":
                results = results.filter(network__uuid=filter_uuid)
            elif filter_type == "Job Title":
                results = results.filter(Exists(JobTitle.objects
                                                .filter(uuid=filter_uuid,
                                                        ratereport__season=OuterRef('pk'))))

        job_report_sq = (Season.objects
                               .filter(id=OuterRef('pk'))
                               .annotate(
                                    job_report=JSONObject(
                                        job_title=JSONObject(
                                            title='ratereport__job_title__title',
                                            uuid='ratereport__job_title__uuid'),
                                        reports=JSONBAgg(JSONObject(
                                            daily='ratereport__final_daily',
                                            hourly='ratereport__final_hourly',
                                            guarantee='ratereport__final_guarantee',
                                            increase='ratereport__percent_increase'),
                                            ordering='ratereport__final_hourly'))))

        if filter_type and filter_type == "Job Title":
            job_report_sq = job_report_sq.filter(job_report__job_title__uuid=filter_uuid)

        results = (results.annotate(job_reports=ArraySubquery(job_report_sq.values('job_report')))
                          .values('uuid',
                                  'start_date',
                                  'end_date',
                                  'genre',
                                  'job_reports',
                                  season_title=F('title'),
                                  union_status=F('union'),
                                  show_title=F('show__title'),
                                  show_uuid=F('show__uuid'),
                                  network_name=F('network__name'),
                                  network_uuid=F('network__uuid'),
                                  company_list=JSONBAgg(JSONObject(name='companies__name',
                                                                   uuid='companies__uuid'),
                                                        ordering='companies__name')
                                  ).order_by('-start_date', 'uuid')
                   )

        if filter_type and filter_type == "Company":
            results = results.filter(companies__uuid=filter_uuid)

        results = self.paginate_queryset(results, request)

        if results is not None:
            serializer = SeasonSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SummaryAPIView(APIView):
    BIN_SIZE = 5

    def get(self, request): # noqa
        date_range = request.GET.get('date_range', '')
        if date_range.isnumeric():
            date_range = int(date_range)
        union_select = request.GET.get('union_select', '')
        genre_select = request.GET.get('genre_select', '')
        filter_uuid = request.GET.get('filter_uuid', '')
        filter_type = request.GET.get('filter_type', '')

        bins = {}
        statistics = {}
        rate_count = 0

        results = Season.objects.all()

        if date_range:
            duration = timedelta(days=(30 * date_range))
            date_limit = date.today() - duration
            results = results.filter(start_date__gte=date_limit)

        if union_select != 'AA':
            results = results.filter(union__exact=union_select)

        if genre_select != 'AA':
            results = results.filter(genre__exact=genre_select)

        summary_base = results

        if filter_uuid and filter_type:
            filtered_rate_reports = summary_base.filter(ratereport__job_title__uuid=filter_uuid)

            bins = (filtered_rate_reports
                         .annotate(bin_floor=Cast(
                            Floor(F('ratereport__final_hourly') /
                                  self.BIN_SIZE) * self.BIN_SIZE,
                            output_field=IntegerField())).values('bin_floor')
                         .order_by('bin_floor').annotate(count=Count('bin_floor'))
                         .aggregate(bins=JSONBAgg(JSONObject(bin_floor='bin_floor',
                                                             count='count'),
                                                  ordering='bin_floor')))['bins']

            rate_count = filtered_rate_reports.count()

            statistics = filtered_rate_reports.aggregate(min=Min('ratereport__final_hourly'),
                                                         med=Median('ratereport__final_hourly'),
                                                         max=Max('ratereport__final_hourly'))
        summary = {
            'histogram': {
                'bins': bins,
                'bin_size': self.BIN_SIZE,
                'med': statistics["med"] if statistics else 0
            },
            'rate_count': rate_count,
            'statistics': statistics
        }
        serializer = SummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterSearchAPIView(APIView):

    def get(self, request): # noqa
        q = request.GET.get('q', '')
        if q:
            show_matches = (Show.objects.filter(title__icontains=q).filter(Exists(
                RateReport.objects.filter(season__show=OuterRef('pk'))))
                            .aggregate(options=JSONBAgg(JSONObject(
                                                label='title', type=Value('Show'), value='uuid'),
                                                ordering='title')))

            company_matches = (Company.objects.filter(name__icontains=q).filter(Exists(
                RateReport.objects.filter(season__companies=OuterRef('pk'))))
                                  .aggregate(options=JSONBAgg(JSONObject(
                                            label='name', type=Value('Company'), value='uuid'),
                                            ordering='name')))

            network_matches = (Network.objects.filter(name__icontains=q).filter(Exists(
                RateReport.objects.filter(season__network=OuterRef('pk'))))
                               .aggregate(options=JSONBAgg(JSONObject(
                                         label='name', type=Value('Network'), value='uuid'),
                                         ordering='name')))

            job_title_matches = (JobTitle.objects.filter(title__icontains=q).filter(Exists(
                RateReport.objects.filter(job_title=OuterRef('pk'))))
                                  .aggregate(options=JSONBAgg(JSONObject(
                                            label='title', type=Value('Job Title'), value='uuid'),
                                            ordering='title')))

            all_matches = (show_matches['options'] + company_matches['options'] +
                           network_matches['options'] + job_title_matches['options'])
            all_matches.sort(key=lambda option: option['label'])

            data = FilterSearchSerializer(all_matches, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)
