from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Season


@login_required
def discover(request):
    template = loader.get_template('rates/discover.html')
    context = {
        'apiUrls': {
            'autocomplete': reverse('autocomplete'),
            'details': reverse('details'),
            'shows': reverse('shows'),
            'companies': reverse('companies'),
            'networks': reverse('networks'),
            'job-titles': reverse('job-titles'),
            'add-rate-api': reverse('add-rate-api')
        }
    }
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
            'job-titles': reverse('job-titles'),
            'add-rate-api': reverse('add-rate-api')
        }
    }
    return HttpResponse(template.render(context, request))


class ContactFormView(FormView):
    template_name = 'rates/contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        form.save()
        form = ContactForm()
        return super().form_valid(form)


def thanks(request):
    template = loader.get_template('rates/thanks.html')
    context = {}
    return HttpResponse(template.render(context, request))