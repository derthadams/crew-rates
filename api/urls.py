from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^autocomplete/$', views.LocationAutocompleteAPIView.as_view(),
            name='autocomplete'),
    re_path(r'^details/$', views.LocationDetailsAPIView.as_view(),
            name='details'),
    re_path(r'^job-titles/$', views.JobTitlesAPIView.as_view(),
            name='job-titles'),
    re_path(r'^shows/$', views.ShowsAPIView.as_view(),
            name='shows'),
    re_path(r'^companies/$', views.CompaniesAPIView.as_view(),
            name='companies'),
    re_path(r'^networks/$', views.NetworksAPIView.as_view(),
            name='networks'),
]
