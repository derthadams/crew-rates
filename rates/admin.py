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


class SeasonCompanyInline(admin.TabularInline):
    model = Season.companies.through
    ordering = ('season__title',)
    readonly_fields = ['season']
    can_delete = False
    verbose_name = 'Seasons'
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


class RateReportInline(admin.TabularInline):
    model = RateReport
    ordering = ('job_title',)
    fields = ['user', 'job_title', 'hourly', 'guarantee']
    readonly_fields = ['user', 'job_title', 'hourly', 'guarantee', 'season']
    can_delete = False
    extra = 0
    max_num = 0
    template = 'admin/rates/company/edit_inline/tabular.html'


class CompanyAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    inlines = [SeasonCompanyInline]
    list_display = ('name', 'id',)


class ShowAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']
    inlines = [SeasonInline]
    list_display = ('title', 'id',)


class NetworkAdmin(admin.ModelAdmin):
    ordering=['name']
    search_fields = ['name']
    inlines = [SeasonInline]
    list_display = ('name', 'id',)


class LocationAdmin(admin.ModelAdmin):
    ordering = ['display_name']
    search_fields = ['display_name']
    list_display = ('display_name', 'id',)


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
    list_display = ('title', 'id')


@admin.action(description="Approve raw rate report")
def approve_raw_rate_report(modeladmin, request, queryset):
    for raw_report in queryset:
        if raw_report.job_title == -1:
            job_title_obj = JobTitle.objects.get_or_create(
                title=raw_report.job_title_name)
            job_title = job_title_obj[0].pk
        else:
            job_title = raw_report.job_title

        if raw_report.show == -1:
            show_obj = Show.objects.get_or_create(
                title=raw_report.show_title)
            show = show_obj[0].pk
        else:
            show = raw_report.show

        #TODO: Implement multiple companies
        # if raw_report.companies == -1:
        #     companies_obj = Company.objects.get_or_create(
        #         name=raw_report.company_name)
        #     company = companies_obj[0].pk
        # else:
        #     company_id = raw_report.company_id

        if raw_report.network == -1:
            network_obj = Network.objects.get_or_create(
                name=raw_report.network_name)
            network = network_obj[0].pk
        else:
            network = raw_report.network

        if raw_report.locations:
            locations = set()
            scopes = set()
            for location in raw_report.locations['locations']:
                location_object = make_location_object(location['scopes'][0])
                locations.add(location_object[0].id)
                scopes.add(location_object[0].id)

                for i in range(1, len(location['scopes'])):
                    scope_object = make_location_object(location['scopes'][i])
                    scopes.add(scope_object[0].id)
            locations = list(locations)
            scopes = list(scopes)
        else:
            locations = []
            scopes = []

        seasons = Season.objects.filter(
            show__id=show,
            number=raw_report.season_number
        )
        if len(seasons):
            season = seasons[0]

            if not season.start_date and not season.end_date:
                season.start_date = raw_report.start_date
                season.end_date = raw_report.end_date

            #TODO: Implement multiple companies
            # season.companies.add(company_id)

            if not season.network:
                season.network_id = network

            season.locations.add(*locations)
            season.scopes.add(*scopes)

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

            # TODO: Implement multiple companies
            # season.companies.add(company_id)
            season.locations.add(*locations)
            season.scopes.add(*scopes)

        RateReport.objects.create(
            user=raw_report.user,
            job_title_id=job_title,
            hourly=raw_report.hourly,
            guarantee=raw_report.guarantee,
            season=season,
            union=raw_report.union,
            raw_report=raw_report
        )

        raw_report.approved = True
        raw_report.save()


def make_location_object(location_dict):
    return Location.objects.get_or_create(
        display_name=location_dict['display_name'],
        long_name=location_dict['long_name'],
        short_name=location_dict['short_name'],
        type=location_dict['type']
    )


class RawRateReportAdmin(admin.ModelAdmin):
    actions = [approve_raw_rate_report]
    list_filter = ('approved',)


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobTitle)
admin.site.register(Show, ShowAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(RawRateReport, RawRateReportAdmin)
admin.site.register(RateReport)
