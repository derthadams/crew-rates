from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware
from django.template import loader
from django.urls import reverse
from django.views import View
from .forms import RawRateReportForm

import json


@login_required
def index(request):
    template = loader.get_template('rates/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


class AddRateView(View):
    def get(self, request, *args, **kwargs):
        form = RawRateReportForm()
        return render(request, 'rates/add_rate.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # sample_data = json.dumps({
        #     "job_title": 1,
        #     "job_title_name": "Camera Operator",
        #     "hourly": 54.5454,
        #     "guarantee": 10,
        #     "show": 1,
        #     "show_title": "Project Roonway",
        #     "season_number": 4,
        #     "companies": {},
        #     "network": 1,
        #     "network_name": "Bravo",
        #     "locations": {},
        #     "start_date": "2021-01-01",
        #     "end_date": "2021-02-01",
        #     "union": "IA",
        #     "genre": "RE",
        # })
        # print(request.body)
        # print(f"request body type:{type(request.body)}")
        data = json.loads(request.body)
        # data = json.loads(sample_data)
        headers = dict(request.headers)

        data['user'] = request.user.id
        # data['user'] = 1

        # print(json.dumps(data, indent=4))
        # print(json.dumps(headers, indent=4))

        # form = RawRateReportForm(data)
        form = RawRateReportForm(data)

        # print(form.is_bound)

        if form.is_valid():
            # print("Form valid")
            form.save()
            return HttpResponseRedirect(reverse('thanks'))
        else:
            # print("Form not valid")
            # print(form.errors)
            # return HttpResponse("Form not valid")
            # return render(request, 'rates/add_rate.html', {'form': form})
            context = {'form': form}
            # print(f"context: \n{context}")
            return render(request, 'rates/add_rate.html', context)


def thanks(request):
    template = loader.get_template('rates/thanks.html')
    context = {}
    return HttpResponse(template.render(context, request))
