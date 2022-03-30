from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django.forms import NullBooleanSelect, Textarea
from django.utils.translation import gettext_lazy as _


from .models import User, Company, JobTitle, Show, Network, Location, Season, \
    RawRateReport, RateReport, RatesInvitation
from invitations.forms import InvitationAdminAddForm, InvitationAdminChangeForm


def calc_delta(final, offered):
    return round(((final - offered) / offered) * 100)


def calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily):
    if final_hourly > offered_hourly and final_daily >= offered_daily:
        hourly_delta = calc_delta(final_hourly, offered_hourly)
    else:
        hourly_delta = 0

    if final_daily > offered_daily and final_hourly >= offered_hourly:
        daily_delta = calc_delta(final_daily, offered_daily)
    else:
        daily_delta = 0

    if hourly_delta == 0 and daily_delta == 0:
        return None
    else:
        return max(hourly_delta, daily_delta)


def _approve_raw_rate_report(raw_report):
    uuid_null = '00000000-0000-0000-0000-000000000000'
    if raw_report.job_title_override: # noqa
        job_title = raw_report.job_title_override.id
    else:
        if raw_report.job_title == uuid_null:
            job_title_obj, created = JobTitle.objects.get_or_create( # noqa
                title=raw_report.job_title_name)
        else:
            job_title_obj = JobTitle.objects.get(uuid=raw_report.job_title) # noqa
        job_title = job_title_obj.pk

    if raw_report.show_override: # noqa
        show = raw_report.show_override.id
    else:
        if raw_report.show == uuid_null:
            show_obj, created = Show.objects.get_or_create( # noqa
                title=raw_report.show_title)
        else:
            show_obj = Show.objects.get(uuid=raw_report.show) # noqa
        show = show_obj.pk

    companies = []
    if len(raw_report.companies_override.all()) > 0:
        companies = list(raw_report.companies_override.all().values_list('id', flat=True))
    else:
        for company in raw_report.companies:
            if company['uuid'] == uuid_null:
                company_obj, created = Company.objects.get_or_create( # noqa
                    name=company['name'])
            else:
                company_obj = Company.objects.get(uuid=company['uuid']) # noqa
            companies.append(company_obj.pk)

    network = None
    if raw_report.network_override:
        network = raw_report.network_override.id
    else:
        if raw_report.network:
            if raw_report.network == uuid_null:
                network_obj, created = Network.objects.get_or_create( # noqa
                    name=raw_report.network_name)
            else:
                network_obj = Network.objects.get(uuid=raw_report.network) # noqa
            network = network_obj.pk

    if raw_report.locations:
        locations_set = set()
        scopes_set = set()

        for location in raw_report.locations:
            location_object, created = make_location_object(location['scopes'][0],
                                                            location['latitude'],
                                                            location['longitude'])
            locations_set.add(location_object.id)
            scopes_set.add(location_object.id)

            for i in range(1, len(location['scopes'])):
                scope_object, created = make_location_object(location['scopes'][i])
                scopes_set.add(scope_object.id)
        locations = list(locations_set)
        scopes = list(scopes_set)
    else:
        locations = []
        scopes = []

    seasons = Season.objects.filter( # noqa
        show__id=show,
        number=raw_report.season_number
    )
    if len(seasons):
        season = seasons[0]

        if not season.start_date and not season.end_date:
            season.start_date = raw_report.start_date
            season.end_date = raw_report.end_date

        if not season.network:
            season.network_id = network

        season.locations.add(*locations)
        season.scopes.add(*scopes)
        season.companies.add(*companies)

        if not season.genre:
            season.genre = raw_report.genre

        if not season.union and raw_report.union:
            season.union = True

        season.save()

    else:
        season = Season.objects.create(
            show_id=show,
            number=raw_report.season_number,
            start_date=raw_report.start_date,
            end_date=raw_report.end_date,
            union=raw_report.union,
            network_id=network,
            genre=raw_report.genre
        )

        season.locations.add(*locations)
        season.scopes.add(*scopes)
        season.companies.add(*companies)

    percent_increase = 0
    if raw_report.increased:
        percent_increase = calc_percent_increase(raw_report.final_hourly,
                                                 raw_report.final_daily,
                                                 raw_report.offered_hourly,
                                                 raw_report.offered_daily)

    RateReport.objects.create(
        user=raw_report.user,
        job_title_id=job_title,
        offered_daily=raw_report.offered_daily,
        offered_hourly=raw_report.offered_hourly,
        offered_guarantee=raw_report.offered_guarantee,
        negotiated=raw_report.negotiated,
        increased=raw_report.increased,
        final_daily=raw_report.final_daily,
        final_hourly=raw_report.final_hourly,
        final_guarantee=raw_report.final_guarantee,
        season=season,
        union=raw_report.union,
        raw_report=raw_report,
        percent_increase=percent_increase
    )

    raw_report.approved = True
    raw_report.save()


@admin.action(description="Approve raw rate report")
def approve_raw_rate_report(modeladmin, request, queryset):
    for raw_report in queryset:
        _approve_raw_rate_report(raw_report)
        raw_report.delete()


def make_location_object(location_dict, latitude=None, longitude=None):
    location, created = Location.objects.get_or_create(
        display_name=location_dict['display_name'],
        long_name=location_dict['long_name'],
        short_name=location_dict['short_name'],
        type=location_dict['type'])
    if not latitude and not longitude:
        return location, created
    if latitude and not location.latitude:
        location.latitude = latitude
    if longitude and not location.longitude:
        location.longitude = longitude
    location.save()
    return location, created


"""
------------------- INLINE CLASSES -----------------------
"""


class RateReportInline(admin.TabularInline):
    model = RateReport
    ordering = ('job_title',)
    fields = ['user', 'job_title', 'offered_hourly', 'offered_guarantee', 'final_hourly',
              'final_guarantee']
    readonly_fields = ['user', 'job_title', 'offered_hourly', 'offered_guarantee', 'final_hourly',
                       'final_guarantee', 'season']
    can_delete = False
    extra = 0
    max_num = 0
    template = 'admin/rates/company/edit_inline/tabular.html'


class SeasonInline(admin.TabularInline):
    model = Season
    ordering = ('title',)
    readonly_fields = ['title', 'show', 'number', 'start_date', 'end_date',
                       'union', 'companies', 'network', 'locations', 'scopes',
                       'genre']
    can_delete = False
    extra = 0
    max_num = 0
    template = 'admin/rates/company/edit_inline/tabular.html'


class SeasonCompanyInline(admin.TabularInline):
    model = Season.companies.through
    ordering = ('season__title',)
    readonly_fields = ['season']
    can_delete = False
    verbose_name = 'Seasons'
    verbose_name_plural = 'Seasons'
    extra = 0
    max_num = 0
    template = 'admin/rates/company/edit_inline/tabular.html'


"""
---------------------- ADMIN CLASSES ---------------------------
"""


class CompanyAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    inlines = [SeasonCompanyInline]
    list_display = ('name', 'created_at', 'id',)


class JobTitleAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'uuid',
    ]
    readonly_fields = [
        'uuid'
    ]
    search_fields = ['title', 'uuid']


class LocationAdmin(admin.ModelAdmin):
    ordering = ['display_name']
    search_fields = ['display_name', 'type', 'latitude', 'longitude']
    list_display = ('display_name', 'type', 'latitude', 'longitude', 'id',)


class NetworkAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    inlines = [SeasonInline]
    list_display = ('name', 'id',)


class RateReportAdmin(admin.ModelAdmin):
    search_fields = ['season__title', 'job_title__title']
    list_display = ('season', 'job_title', 'final_hourly', 'final_guarantee', 'created_at')


class RawRateReportAdmin(admin.ModelAdmin):
    actions = [approve_raw_rate_report]
    autocomplete_fields = [
        'company_matches',
        'companies_override',
        'job_title_matches',
        'job_title_override',
        'network_matches',
        'network_override',
        'show_matches',
        'show_override'
    ]
    fieldsets = (
        (None, {
            'fields': ('user', ('approved', 'user_created_values')),
        }),
        (None, {
            'fields': (('job_title_name', 'job_title'), ('job_title_matches',),
                       ('job_title_override',))
        }),
        (None,
         {
             'fields': (('offered_hourly', 'offered_daily', 'offered_guarantee'),
                        ('negotiated', 'increased',),
                        ('final_hourly', 'final_daily', 'final_guarantee'))
         }),
        (None, {
            'fields': (('show_title', 'show', 'season_number'),
                       ('show_matches', ), ('show_override',)),
        }),
        (None, {
            'fields': (('genre', 'union'),
                       'start_date', 'end_date')
        }),
        (None, {
            'fields': (('companies',), ('company_matches',), ('companies_override',))
        }),
        (None, {
            'fields': (('network_name', 'network'), ('network_matches', ), ('network_override',))
        }),
        (None, {
            'fields': ('locations',)
        }),
        (None, {
            'fields': (('created_at', 'modified_at'),)
        })
    )

    formfield_overrides = {
        models.JSONField: {
            'widget': Textarea(
                attrs={'rows': 3, 'cols': 70}
            )
        },
        models.BooleanField: {
            'widget': NullBooleanSelect()
        }
    }
    list_display = ('user', 'show_title', 'season_number', 'job_title_name', 'final_hourly',
                    'final_guarantee', 'created_at')
    list_filter = ('approved',)

    readonly_fields = ['created_at', 'modified_at']


class SeasonAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = [
        'companies',
        'show',
        'network',
        'locations',
        'scopes'
    ]
    inlines = [RateReportInline]
    list_display = ('title', 'number', 'id')


class ShowAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']
    inlines = [SeasonInline]
    list_display = ('title', 'id',)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', ('first_name', 'last_name'), 'preferred_name', 'password',
                           'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'preferred_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class RatesInvitationAdminAddForm(InvitationAdminAddForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        widget=forms.TextInput(attrs={"type": "text", "size": "30"})
    )

    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        widget=forms.TextInput(attrs={"type": "text", "size": "30"})
    )

    preferred_name = forms.CharField(
        label=_("Preferred name"),
        required=False,
        widget=forms.TextInput(attrs={"type": "text", "size": "30"})
    )

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get('last_name')
        preferred_name = cleaned_data.get('preferred_name')
        params = {'email': email, 'first_name': first_name, 'last_name': last_name,
                  'preferred_name': preferred_name}
        if cleaned_data.get("inviter"):
            params['inviter'] = cleaned_data.get("inviter")
        instance = RatesInvitation.create(**params)
        instance.send_invitation(self.request)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = RatesInvitation
        fields = ("email", "first_name", "last_name", "preferred_name", "inviter")


class RatesInvitationAdminChangeForm(InvitationAdminChangeForm):

    class Meta:
        model = RatesInvitation
        fields = '__all__'


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(RawRateReport, RawRateReportAdmin)
admin.site.register(RateReport, RateReportAdmin)
