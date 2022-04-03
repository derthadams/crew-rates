from allauth.socialaccount.models import SocialAccount, SocialToken

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
from .signals import social_account_removed

genreOptions = [{
        'value': value,
        'label': label
    } for value, label in Season.GENRE_CHOICES]

unionOptions = [{
        'value': value,
        'label': label
    } for value, label in Season.UNION_CHOICES
]


@login_required
def discover(request):
    template = loader.get_template('rates/discover.html')
    context = {
        'genre': dict(Season.GENRE_CHOICES),
        'unionStatus': dict(Season.UNION_CHOICES),
        'genreOptions': genreOptions,
        'unionOptions': unionOptions,
        'apiUrls': {
            'season-list': reverse('season-list'),
            'filter-search': reverse('filter-search'),
            'summary': reverse('summary')
        }
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_rate(request, path=""):
    template = loader.get_template('rates/add-rate.html')
    context = {
        'genreOptions': genreOptions,
        'unionOptions': unionOptions,
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

        if form.is_valid() and form.cleaned_data['delete_field'] == "DELETE":
            user_to_delete = User.objects.get(email=request.user)
            if user_to_delete is not None:
                social_accounts = SocialAccount.objects.filter(user_id=user_to_delete.pk)
                if social_accounts:
                    for account in social_accounts:
                        social_token = SocialToken.objects.filter(account_id=account.pk)
                        if social_token:
                            social_account_removed.send(
                                sender=SocialAccount, request=request, socialaccount=account,
                                socialtoken=social_token[0]
                            )
                user_to_delete.delete()
                logout(request)
                messages.info(request, "We're sorry to see you go! "
                                       "Your account has been deleted.")
                messages.info(request,
                              "If you want to return, you're always welcome to "
                              "request a new invitation.")
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


def home(request):
    template = loader.get_template('rates/home.html')
    context = {}
    return HttpResponse(template.render(context, request))