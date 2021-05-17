from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware
from django.template import loader
from django.views import View
from .forms import RawRateReportForm

import json
import pprint


@login_required
def index(request):
    template = loader.get_template('rates/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


class AddRateView(View):
    def get(self, request, *args, **kwargs):
        form = RawRateReportForm()
        return render(request, 'rates/test_add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        headers = dict(request.headers)

        data['user'] = request.user.id
        form = RawRateReportForm(data=data)

        print(json.dumps(data, indent=4))
        pprint.pprint(headers)

        if form.is_valid():
            print("Form valid")
            form.save()
            return HttpResponseRedirect('/thanks/')
        else:
            print("Form not valid")
            return HttpResponse("Form not valid")


def thanks(request):
    template = loader.get_template('rates/thanks.html')
    context = {}
    return HttpResponse(template.render(context, request))
