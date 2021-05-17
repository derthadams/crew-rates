from django.forms import ModelForm, HiddenInput, DateInput, RadioSelect, \
    Select, SelectMultiple
from .models import RawRateReport


class RawRateReportForm(ModelForm):
    class Meta:
        model = RawRateReport
        exclude = [
            'user',
            'approved'
        ]
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
            'job_title_id': HiddenInput(),
            'job_title_name': Select(),
            'hourly': HiddenInput(),
            'guarantee': HiddenInput(),
            'show_id': HiddenInput(),
            'network_id': HiddenInput(),
            'network_name': Select(),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            # 'union': RadioSelect(),
            'companies': SelectMultiple,
            'locations': SelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
