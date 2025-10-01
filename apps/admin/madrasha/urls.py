from django.urls import path
from .views import (
    MadrashaListView,
    MadrashaCacheManagementView,
    DivisionListView,
    DistrictListView,
    ThanaListView
)

urlpatterns = [
    path('madrasha-list/', MadrashaListView.as_view(), name='madrasha-list'),
    path('cache/', MadrashaCacheManagementView.as_view(), name='madrasha-cache-management'),
    # Filter dropdown endpoints
    path('divisions/', DivisionListView.as_view(), name='division-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('thanas/', ThanaListView.as_view(), name='thana-list'),
]
