from django.core import exceptions, validators
from django.forms import Form, ModelForm, HiddenInput, DateInput, RadioSelect, \
    Select, SelectMultiple, ModelChoiceField, BooleanField, TextInput, EmailField, CharField, \
    ValidationError
from django.utils.translation import gettext_lazy as _, pgettext
from .models import RawRateReport
from .adapters import get_adapter

from allauth.socialaccount.models import SocialAccount, SocialToken
from .signals import social_account_removed

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.forms import PasswordField
# from allauth.account.app_settings import AppSettings
from allauth.account import app_settings
from allauth.account.utils import perform_login
from allauth.utils import get_username_max_length, set_form_field_order
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # pass
            self.fields[field].widget.attrs.update({'class': 'form-control',
                                                    'autocomplete': 'off'})


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


class LoginForm(Form):

    password = PasswordField(label=_("Password"), autocomplete="current-password")
    remember = BooleanField(label=_("Remember Me"), required=False)

    user = None
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
            login_field = EmailField(label=_("E-mail"), widget=login_widget)
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

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        login = self.cleaned_data["login"]
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            credentials["email"] = login
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            credentials["username"] = login
        else:
            if self._is_login_email(login):
                credentials["email"] = login
            credentials["username"] = login
        credentials["password"] = self.cleaned_data["password"]
        return credentials

    def clean_login(self):
        login = self.cleaned_data["login"]
        return login.strip()

    def _is_login_email(self, login):
        try:
            validators.validate_email(login)
            ret = True
        except exceptions.ValidationError:
            ret = False
        return ret

    def clean(self):
        super(LoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user = get_account_adapter(self.request).authenticate(self.request, **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data["login"]
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            raise ValidationError(
                self.error_messages["%s_password_mismatch" % auth_method]
            )
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        email = self.user_credentials().get("email")
        ret = perform_login(
            request,
            self.user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=redirect_url,
            email=email,
        )
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data["remember"]
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret
