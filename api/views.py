from django.apps import apps
from django.db.models import F
from django.views import View
from django.http import JsonResponse
import requests
from .api_config import *


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


class JobTitlesAPIView(View):
    def get(self, request, *args, **kwargs):
        job_title = apps.get_model('rates', 'JobTitle')
        results = list(
            job_title.objects.filter(
                title__icontains=self.request.GET.get('q')
            )
            .annotate(text=F('title'))
            .values('id', 'text'))
        return JsonResponse({"results": results})


class ShowsAPIView(View):
    def get(self, request, *args, **kwargs):
        show = apps.get_model('rates', 'Show')
        results = list(
            show.objects.filter(
                title__icontains=self.request.GET.get('q')
            )
            .annotate(text=F('title'))
            .values('id', 'text'))
        return JsonResponse({"results": results})


class CompaniesAPIView(View):
    def get(self, request, *args, **kwargs):
        company = apps.get_model('rates', 'Company')
        results = list(
            company.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(text=F('name'))
            .values('id', 'text'))
        return JsonResponse({"results": results})


class NetworksAPIView(View):
    def get(self, request, *args, **kwargs):
        network = apps.get_model('rates', 'Network')
        results = list(
            network.objects.filter(
                name__icontains=self.request.GET.get('q')
            )
            .annotate(text=F('name'))
            .values('id', 'text'))
        return JsonResponse({"results": results})
