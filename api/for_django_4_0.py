from django.contrib.postgres.aggregates import JSONBAgg
from django.contrib.postgres.expressions import ArraySubquery # noqa
from django.db.models import F, OuterRef
from django.db.models.functions import JSONObject

from rates.models import Season # noqa

"""
Do filtering by:
    Show
    Company
    Network
    Job Title
    Date Range
    Union
    Genre
    
then:
"""

qs = Season.objects.filter(id=OuterRef('pk')).annotate(
        job_report=JSONObject(
                        job_title=JSONObject(
                            title='ratereport__job_title__title',
                            uuid='ratereport__job_title__uuid'),
                        reports=JSONBAgg(JSONObject(
                                    daily='ratereport__final_daily',
                                    hourly='ratereport__final_hourly',
                                    guarantee='ratereport__final_guarantee',
                                    increase='ratereport__percent_increase'))))

query = Season.objects.annotate(job_reports=ArraySubquery(qs.values('job_report'))).values(
    'uuid',
    'start_date',
    'end_date',
    'genre',
    'job_reports',
    season_title=F('title'),
    union_status=F('union'),
    show_title=F('show__title'),
    show_uuid=F('show__uuid'),
    network_name=F('network__name'),
    network_uuid=F('network__uuid'),
    company_list=JSONBAgg(JSONObject(name='companies__name',
                                     uuid='companies__uuid'),
                          ordering='companies__name'))
