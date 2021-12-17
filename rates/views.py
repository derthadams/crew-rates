from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RawRateReportForm


@login_required
def index(request):
    template = loader.get_template('rates/discover.html')
    context = {}
    return HttpResponse(template.render(context, request))


class AddRateView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = RawRateReportForm()
        return render(request, 'rates/add_rate.html', {'form': form})


@login_required
def thanks(request):
    template = loader.get_template('rates/thanks.html')
    context = {}
    return HttpResponse(template.render(context, request))
