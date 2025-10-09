from django.urls import path
from .views import (
    MarkazCenterListView,
    MarkazCacheManagementView,
    DivisionListView,
    DistrictListView,
    ThanaListView,
    CenterListView,
    MarkazStatusUpdateView,
    MarkazStatisticsView
)

urlpatterns = [
    path('markaz-list/', MarkazCenterListView.as_view(), name='markaz-list'),
    path('cache/', MarkazCacheManagementView.as_view(), name='markaz-cache-management'),
    path('statistics/', MarkazStatisticsView.as_view(), name='markaz-statistics'),
    # Filter dropdown endpoints
    path('divisions/', DivisionListView.as_view(), name='markaz-division-list'),
    path('districts/', DistrictListView.as_view(), name='markaz-district-list'),
    path('thanas/', ThanaListView.as_view(), name='markaz-thana-list'),
    path('centers/', CenterListView.as_view(), name='markaz-center-list'),
    # Update status
    path('status/<int:pk>/', MarkazStatusUpdateView.as_view(), name='markaz-status-update'),
]