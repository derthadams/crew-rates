from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import RawRateReportForm
from .models import Season


@login_required
def discover(request):
    template = loader.get_template('rates/discover.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def add_rate(request, path=''):
    template = loader.get_template('rates/add-rate.html')
    context = {
        'genreOptions': [
            {
                'value': value,
                'label': label
            } for value, label in Season.GENRE_CHOICES
        ],
        'unionOptions': [
            {
                'value': value,
                'label': label
            } for value, label in Season.UNION_CHOICES
        ],
        'apiUrls': {
            'autocomplete': reverse('autocomplete'),
            'details': reverse('details'),
            'shows': reverse('shows'),
            'companies': reverse('companies'),
            'networks': reverse('networks'),
            'job-titles': reverse('job-titles')
        }
    }
    return HttpResponse(template.render(context, request))
