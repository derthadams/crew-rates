from django.contrib.postgres.fields import ArrayField
from django.db.models import Aggregate, DecimalField, Subquery
from django.utils.functional import cached_property


class ArraySubquery(Subquery): # noqa
    template = "ARRAY(%(subquery)s)"

    def __init__(self, queryset, **kwargs):
        super().__init__(queryset, **kwargs)

    @cached_property
    def output_field(self):
        return ArrayField(self.query.output_field)


class Median(Aggregate): # noqa
    function = 'PERCENTILE_DISC'
    name = 'median'
    output_field = DecimalField()
    template = '%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)'
