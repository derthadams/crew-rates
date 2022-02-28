from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ContactForm, DeleteUser
from .models import Season, User


@login_required
def discover(request):
    template = loader.get_template('rates/discover.html')
    context = {
        'genre': dict(Season.GENRE_CHOICES),
        'unionStatus': dict(Season.UNION_CHOICES),
        'apiUrls': {
            'rate-report-list': reverse('rate-report-list')
        }
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_rate(request):
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


@login_required
def settings(request):
    if request.method == 'POST':
        form = DeleteUser(request.POST)

        if form.is_valid():
            if form.cleaned_data['delete_field'] == "DELETE":
                user_to_delete = User.objects.get(email=request.user)
                if user_to_delete is not None:
                    user_to_delete.delete()
                    logout(request)
                    messages.info(request, "We're sorry to see you go! "
                                           "Your account has been deleted.")
                    messages.info(request,
                                  "If you ever want to rejoin, please request a new invitation.")
                    return redirect(reverse("account_login"))
                else:
                    messages.error(request, "There was an error in deleting your account.")
    else:
        form = DeleteUser()
    context = {'form': form}
    return render(request, 'settings.html', context)


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