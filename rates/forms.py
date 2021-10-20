from django.forms import Form, ModelForm, HiddenInput, DateInput, RadioSelect, \
    Select, SelectMultiple, ModelChoiceField
from .models import RawRateReport
from .adapters import get_adapter

from allauth.socialaccount.models import SocialAccount, SocialToken
from .signals import social_account_removed


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
            # self.fields[field].widget.attrs.update({'autocomplete': 'off'})


class DisconnectForm(Form):
    account = ModelChoiceField(
        queryset=SocialAccount.objects.none(),
        widget=RadioSelect,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        print("IN DISCONNECT FORM")
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
        # print(f"Token from save(): {token}")
        account.delete()
        social_account_removed.send(
            sender=SocialAccount, request=self.request, socialaccount=account,
            socialtoken=socialtoken
        )