from django.forms import ModelForm, HiddenInput, DateInput, RadioSelect, \
    Select, SelectMultiple
from .models import RawRateReport


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
            'job_title_name': Select(attrs={'required': 'required'}),
            'hourly': HiddenInput(),
            'guarantee': HiddenInput(),
            'show': HiddenInput(),
            'show_title': Select(attrs={'required': 'required'}),
            'network': HiddenInput(),
            'network_name': Select(attrs={'required': 'required'}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'companies': SelectMultiple,
            'locations': Select(attrs={'multiple': 'multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control',
                                                    'autocomplete': 'off'})
