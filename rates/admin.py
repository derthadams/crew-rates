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
