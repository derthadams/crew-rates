from django.core.mail import send_mail
from django.forms import Form, ModelForm, HiddenInput, DateInput, RadioSelect, \
    Select, ModelChoiceField,  TextInput, EmailField, CharField
from django.utils.translation import gettext_lazy as _, pgettext

from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.account.forms import ResetPasswordForm, LoginForm
from allauth.account import app_settings
from allauth.utils import get_username_max_length, set_form_field_order
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from .adapters import get_adapter
from .models import RawRateReport, Contact, User
from .signals import social_account_removed

AuthenticationMethod = app_settings.AuthenticationMethod


class RawRateReportForm(ModelForm):
    class Meta:
        model = RawRateReport
        fields = '__all__'
        labels = {
            'job_title_name': 'Job Title',
            'show_title': 'Show Title',
            'season_number': 'Season',
            'network_name': 'Network/Streaming Platform',
            'locations': 'Filming Locations',
            'companies': 'Production Companies',
            'union': 'Union Status'
        }
        widgets = {
            'user': HiddenInput(),
            'job_title': HiddenInput(),
            'job_title_name': Select(attrs={'required': 'required',
                                            'class': 'form-select'}),
            'hourly': HiddenInput(),
            'guarantee': HiddenInput(),
            'show': HiddenInput(),
            'show_title': Select(attrs={'required': 'required'}),
            'genre': Select(attrs={'required': 'required'}),
            'union': Select(attrs={'required': 'required'}),
            'network': HiddenInput(),
            'network_name': Select(attrs={'required': 'required'}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'companies': Select(attrs={'multiple': 'multiple'}),
            'locations': Select(attrs={'multiple': 'multiple'}),
        }


class ContactForm(Form):
    email = EmailField()
    name = CharField()
    subject = CharField()
    message = CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def save(self):
        data = self.cleaned_data
        contact = Contact(email=data['email'], name=data['name'], subject=data['subject'],
                          message=data['message'])
        contact.save()

    def send_email(self):
        super_users = User.objects.filter(is_superuser=True)
        emails = map(lambda x: x.email, super_users)
        send_mail(
            f'[{self.cleaned_data["name"]}, {self.cleaned_data["email"]}] '
            f'{self.cleaned_data["subject"]}',
            f'{self.cleaned_data["message"]}',
            'contact@crewrates.org',
            emails,
            fail_silently=False
        )


class DisconnectForm(Form):
    account = ModelChoiceField(
        queryset=SocialAccount.objects.none(),
        widget=RadioSelect,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        # print("IN DISCONNECT FORM")
        self.request = kwargs.pop("request")
        self.accounts = SocialAccount.objects.filter(user=self.request.user)
        super(DisconnectForm, self).__init__(*args, **kwargs)
        self.fields["account"].queryset = self.accounts

    def clean(self):
        cleaned_data = super(DisconnectForm, self).clean()
        account = cleaned_data.get("account")
        if account:
            get_adapter(self.request).validate_disconnect(account, self.accounts)
        return cleaned_data

    def save(self):
        account = self.cleaned_data["account"]
        socialtoken = SocialToken.objects.get(account_id=account.id)
        account.delete()
        social_account_removed.send(
            sender=SocialAccount, request=self.request, socialaccount=account,
            socialtoken=socialtoken
        )


class RatesLoginForm(LoginForm):
    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "The email address and/or password you entered are not correct."
        ),
        "username_password_mismatch": _(
            "The username and/or password you entered are not correct."
        ),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("Email address"),
                    "autocomplete": "email",
                }
            )
            login_field = EmailField(label=_("Email"), widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            login_widget = TextInput(
                attrs={"placeholder": _("Username"), "autocomplete": "username"}
            )
            login_field = CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:
            assert (
                    app_settings.AUTHENTICATION_METHOD
                    == AuthenticationMethod.USERNAME_EMAIL
            )
            login_widget = TextInput(
                attrs={"placeholder": _("Username or email"), "autocomplete": "email"}
            )
            login_field = CharField(
                label=pgettext("field label", "Login"), widget=login_widget
            )
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]


class DeleteUser(Form):
    delete_field = CharField()

    def __init__(self, *args, **kwargs):
        super(DeleteUser, self).__init__(*args, **kwargs)


class RatesResetPasswordForm(ResetPasswordForm):

    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        if self.users:
            self._send_password_reset_mail(request, email, self.users, **kwargs)
        return email

