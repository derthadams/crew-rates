from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .forms import RawRateReportForm


@login_required
def index(request):
    template = loader.get_template('rates/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


class AddRateView(View):
    def get(self, request, *args, **kwargs):
        form = RawRateReportForm()
        return render(request, 'rates/test_add.html', {'form': form})