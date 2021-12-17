import requests

from django.apps import apps
from django.db.models import F
from django.views import View
from django.http import JsonResponse

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .api_config import *
from .serializers import RawRateReportSerializer, JobTitleSerializer, ShowSerializer


class LocationAutocompleteAPIView(View):
    def get(self, request, *args, **kwargs):
        params = {
            "input": self.request.GET.get('q'),
            "sessiontoken": self.request.GET.get('sessiontoken'),
            "key": APIKey,
            "language": "en-US",
            "type": "(regions)"
        }
        response = requests.get(SEARCH_URL, params=params)
        return JsonResponse(response.json())


class LocationDetailsAPIView(View):
    def get(self, request, *args, **kwargs):
        params = {
            "place_id": self.request.GET.get('q'),
            "sessiontoken": self.request.GET.get('sessiontoken'),
            "key": APIKey,
            "language": "en-US"
        }
        response = requests.get(DETAILS_URL, params=params)
        return JsonResponse(response.json())


class JobTitlesAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_title = apps.get_model('rates', 'JobTitle')
        results = list(job_title.objects.filter(
            title__icontains=request.GET.get('q')
        ).annotate(value=F('uuid'), label=F('title')).values('value', 'label'))
        data = JobTitleSerializer(results, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ShowsAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

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


class CompaniesAPIView(View):
    def get(self, request, *args, **kwargs):
        company = apps.get_model('rates', 'Company')
        results = list(
            company.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(value=F('uuid'), label=F('name'))
            .values('value', 'label'))
        return JsonResponse({"results": results})


class NetworksAPIView(View):
    def get(self, request, *args, **kwargs):
        network = apps.get_model('rates', 'Network')
        results = list(
            network.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(value=F('uuid'), label=F('name'))
            .values('value', 'label'))
        return JsonResponse({"results": results})


class AddRate(APIView):
    serializer_class = RawRateReportSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = RawRateReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
