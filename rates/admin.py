from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Company, JobTitle, Show, Network, Location, Season, \
    RawRateReport, RateReport


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login')}),
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

    list_display = ('email', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class CompanyAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class ShowAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']


class NetworkAdmin(admin.ModelAdmin):
    ordering=['name']
    search_fields = ['name']


class LocationAdmin(admin.ModelAdmin):
    ordering = ['display_name']
    search_fields = ['display_name']


class SeasonAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'company',
        'show',
        'network',
        'locations',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobTitle)
admin.site.register(Show, ShowAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(RawRateReport)
admin.site.register(RateReport)


@admin.action(description="Approve raw rate report")
def approve_raw_rate_report(modeladmin, request, queryset):
    for raw_report in queryset:
        if raw_report.job_title_id == -1:
            job_title = JobTitle.objects.get_or_create(
                title=raw_report.job_title_name)
            job_title_id = job_title.pk
        else:
            job_title_id = raw_report.job_title_id

        if raw_report.show_id == -1:
            show = Show.objects.get_or_create(
                title=raw_report.show_title)
            show_id = show.pk
        else:
            show_id = raw_report.show_id

        if raw_report.company_id == -1:
            company = Company.objects.get_or_create(
                name=raw_report.company_name)
            company_id = company.pk
        else:
            company_id = raw_report.company_id

        if raw_report.network_id == -1:
            network = Network.objects.get_or_create(
                name=raw_report.network_name)
            network_id = network.pk
        else:
            network_id = raw_report.network_id

        if raw_report.locations:
            locations = set()
            scopes = set()
            for location in raw_report.locations['locations']:
                location_object = make_location_object(location.scopes[0])
                locations.add(location_object.id)
                scopes.add(location_object.id)

                for i in range(1, len(location.scopes)):
                    scope_object = make_location_object(location.scopes[i])
                    scopes.add(scope_object)
            locations = list(locations)
            scopes = list(scopes)
        else:
            locations = []
            scopes = []

        seasons = Season.objects.filter(
            show__id=show_id,
            number=raw_report.season_number
        )
        if len(seasons):
            season = seasons[0]

            if not season.start_date and not season.end_date:
                season.start_date = raw_report.start_date
                season.end_date = raw_report.end_date

            season.company.add(company_id)

            if not season.network:
                season.network_id = network_id

            season.locations.add(*locations)
            season.scopes.add(*scopes)

            if not season.genre:
                season.genre = raw_report.genre

            season.save()

        else:
            season = Season.objects.create(
                show_id=show_id,
                number=raw_report.season_number,
                start_date=raw_report.start_date,
                end_date=raw_report.end_date,
                union=raw_report.union,
                company_id=company_id,
                network_id=network_id,
                genre=raw_report.genre
            )

            season.locations.add(*locations)
            season.scopes.add(*scopes)

        RateReport.objects.create(
            user=raw_report.user,
            job_title_id=job_title_id,
            hourly=raw_report.hourly,
            guarantee=raw_report.guarantee,
            season=season,
            raw_report=raw_report
        )

        raw_report.approved = True


def make_location_object(location_dict):
    return Location.objects.get_or_create(
        display_name=location_dict.display_name,
        long_name=location_dict.long_name,
        short_name=location_dict.short_name,
        type=location_dict.type
    )
