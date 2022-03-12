from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('autocomplete/', views.LocationAutocompleteAPIView.as_view(), name='autocomplete'),
    path('details/', views.LocationDetailsAPIView.as_view(), name='details'),
    path('add-rate/', views.AddRate.as_view(), name="add-rate-api"),
    path('job-titles/', views.JobTitlesAPIView.as_view(), name='job-titles'),
    path('shows/', views.ShowsAPIView.as_view(), name='shows'),
    path('companies/', views.CompaniesAPIView.as_view(), name='companies'),
    path('networks/', views.NetworksAPIView.as_view(), name='networks'),
    path('season/list/', views.SeasonList.as_view(), name='season-list')
]
