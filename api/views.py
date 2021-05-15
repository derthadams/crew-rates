from django.shortcuts import render
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
    pass


class ShowsAPIView(View):
    pass


class CompaniesAPIView(View):
    pass


class NetworksAPIView(View):
    pass
