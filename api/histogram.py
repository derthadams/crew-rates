from django.db.models import Count, F, IntegerField
from django.db.models.functions import Cast, Floor

from rates.models import RateReport # noqa

results = (RateReport.objects.annotate(bin_floor=Cast(Floor(F('final_hourly')/5)*5,
                                                      output_field=IntegerField()))
                             .values('bin_floor').order_by('bin_floor')
                             .annotate(count=Count('bin_floor'))
                             .values('bin_floor', 'count'))
