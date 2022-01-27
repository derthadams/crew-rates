from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RawRateReportForm


@login_required
def discover(request):
    template = loader.get_template('rates/discover.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def add_rate(request, path=''):
    template = loader.get_template('rates/add-rate.html')
    context = {}
    return HttpResponse(template.render(context, request))
