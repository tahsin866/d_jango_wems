from django.urls import path
from .views import (
    MadrashaListView,
    MadrashaCacheManagementView,
    DivisionListView,
    DistrictListView,
    ThanaListView,
    MadrashaStatusUpdateView
)

urlpatterns = [
    path('madrasha-list/', MadrashaListView.as_view(), name='madrasha-list'),
    path('cache/', MadrashaCacheManagementView.as_view(), name='madrasha-cache-management'),
    # Filter dropdown endpoints
    path('divisions/', DivisionListView.as_view(), name='division-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('thanas/', ThanaListView.as_view(), name='thana-list'),
    # Update status
    path('status/<int:pk>/', MadrashaStatusUpdateView.as_view(), name='madrasha-status-update'),
]
