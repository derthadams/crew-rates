from datetime import date, timedelta
import json
import requests
from uuid import UUID

from django.apps import apps
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import F, DecimalField
from django.db.models.functions import Cast, JSONObject
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rates.models import Season # noqa

from .api_config import *
from .postgres import ArraySubquery
from .queries import job_report_sq
from .serializers import RawRateReportSerializer, RateReportSerializer, JobTitleSerializer, \
    ShowSerializer, CompanySerializer, NetworkSerializer, SeasonSerializer

from rates.admin import _approve_raw_rate_report # noqa
from .sql import season_list


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


class RateReportList(APIView):
    # genre_options = dict(apps.get_model('rates', 'Season').GENRE_CHOICES)
    # union_options = dict(apps.get_model('rates', 'Season').UNION_CHOICES)

    def get(self, request): # noqa
        rate_report = apps.get_model('rates', 'RateReport')
        date_range = request.GET.get('date_range', '')
        if date_range.isnumeric():
            date_range = int(date_range)
        union_select = request.GET.get('union_select', '')
        genre_select = request.GET.get('genre_select', '')

        results = rate_report.objects.all()

        if date_range:
            duration = timedelta(days=(30 * date_range))
            date_limit = date.today() - duration
            results = results.filter(season__start_date__gte=date_limit)

        if union_select != 'AA':
            results = results.filter(season__union__exact=union_select)

        if genre_select != 'AA':
            results = results.filter(season__genre__exact=genre_select)

        results = results.values(
            'uuid',
            'percent_increase',
            'season__start_date',
            'season__end_date',
            guarantee=F('final_guarantee'),
            daily=Cast('final_daily', output_field=DecimalField(
                decimal_places=0,
                max_digits=8)),
            hourly=Cast('final_hourly', output_field=DecimalField(
                decimal_places=2,
                max_digits=7)),
            union_status=F('season__union'),
            show_title=F('season__title'),
            show_uuid=F('season__show__uuid'),
            season_number=F('season__number'),
            genre=F('season__genre'),
            job_title_name=F('job_title__title'),
            job_title_uuid=F('job_title__uuid'),
            network=F('season__network__name'),
            network_uuid=F('season__network__uuid'),
            companies=JSONBAgg(JSONObject(name='season__companies__name',
                                          uuid='season__companies__uuid'),
                               ordering='season__companies__name')
        ).order_by('-season__start_date')
        # companies=ArrayAgg('season__companies__name')

        serializer = RateReportSerializer(results, many=True)
        # if serializer.is_valid():
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeasonList(APIView):

    def get(self, request): # noqa
        date_range = request.GET.get('date_range', '')
        if date_range.isnumeric():
            date_range = int(date_range)
        union_select = request.GET.get('union_select', '')
        genre_select = request.GET.get('genre_select', '')

        results = Season.objects.all()

        if date_range:
            duration = timedelta(days=(30 * date_range))
            date_limit = date.today() - duration
            results = results.filter(start_date__gte=date_limit)

        if union_select != 'AA':
            results = results.filter(union__exact=union_select)

        if genre_select != 'AA':
            results = results.filter(genre__exact=genre_select)

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
                                  ).order_by('-start_date')
                   )

        serializer = SeasonSerializer(results, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
