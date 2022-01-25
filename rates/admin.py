from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, Company, JobTitle, Show, Network, Location, Season, \
    RawRateReport, RateReport, RatesInvitation
from invitations.forms import InvitationAdminAddForm, InvitationAdminChangeForm


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
    fields = ['user', 'job_title', 'offered_hourly', 'offered_guarantee']
    readonly_fields = ['user', 'job_title', 'offered_hourly', 'offered_guarantee', 'season']
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
    uuid_null = '00000000-0000-0000-0000-000000000000'
    for raw_report in queryset:
        if raw_report.job_title == uuid_null:
            job_title_obj, created = JobTitle.objects.get_or_create( # noqa
                title=raw_report.job_title_name)
        else:
            job_title_obj = JobTitle.objects.get(uuid=raw_report.job_title) # noqa
        job_title = job_title_obj.pk

        if raw_report.show == uuid_null:
            show_obj, created = Show.objects.get_or_create( # noqa
                title=raw_report.show_title)
        else:
            show_obj = Show.objects.get(uuid=raw_report.show) # noqa
        show = show_obj.pk

        """
        2021-12-13
        I'm assuming for now that the companies JSON object looks like this:
        
        companies = [
            {
                uuid: "0fa1f64b-58d6-4963-914c-b0711c70e051",
                name: "Magical Elves"
            },
            {
                uuid: None,
                name: "Some New Company
            },
        ]
        """
        companies = []
        for company in raw_report.companies:
            if company['uuid'] == uuid_null:
                company_obj, created = Company.objects.get_or_create(
                    name=company['name'])
            else:
                company_obj = Company.objects.get(uuid=company['uuid'])
            companies.append(company_obj.pk)

        if raw_report.network == uuid_null:
            network_obj, created = Network.objects.get_or_create(
                name=raw_report.network_name)
        else:
            network_obj = Network.objects.get(uuid=raw_report.network)
        network = network_obj.pk

        if raw_report.locations:
            locations_set = set()
            scopes_set = set()

            for location in raw_report.locations:
                location_object, created = make_location_object(location['scopes'][0])
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

        seasons = Season.objects.filter(
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

        RateReport.objects.create(
            user=raw_report.user,
            job_title_id=job_title,
            offered_hourly=raw_report.offered_hourly,
            offered_guarantee=raw_report.offered_guarantee,
            negotiated=raw_report.negotiated,
            increased=raw_report.increased,
            final_hourly=raw_report.final_hourly,
            final_guarantee=raw_report.final_guarantee,
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


class RatesInvitationAdminAddForm(InvitationAdminAddForm):
    name = forms.CharField(
        label=_("Name"),
        required=False,
        widget=forms.TextInput(attrs={"type": "text", "size": "30"})
    )

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name")
        params = {'email': email, 'name': name}
        if cleaned_data.get("inviter"):
            params['inviter'] = cleaned_data.get("inviter")
        instance = RatesInvitation.create(**params)
        instance.send_invitation(self.request)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = RatesInvitation
        fields = ("email", "name", "inviter")


class RatesInvitationAdminChangeForm(InvitationAdminChangeForm):

    class Meta:
        model = RatesInvitation
        fields = '__all__'


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobTitle)
admin.site.register(Show, ShowAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(RawRateReport, RawRateReportAdmin)
admin.site.register(RateReport)
# admin.site.register(RatesInvitation)
