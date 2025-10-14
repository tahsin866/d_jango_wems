from django.urls import path
from .views import (
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentStatisticsView,
    StudentBulkUpdateView,
    StudentSearchView
)
from .field_update_views import (
    StudentFieldUpdateView,
    StudentAddressFieldUpdateView
)
from .test_views import TestStudentAPIView

urlpatterns = [
    # Test API for header-based student fetch
    path('test/', TestStudentAPIView.as_view(), name='test-student-api'),
    
    # Student list with pagination and filtering
    path('', StudentListView.as_view(), name='student-list'),
    
    # Student search
    path('search/', StudentSearchView.as_view(), name='student-search'),
    
    # Student creation
    path('create/', StudentCreateView.as_view(), name='student-create'),
    
    # Student statistics
    path('statistics/', StudentStatisticsView.as_view(), name='student-statistics'),
    
    # Bulk operations
    path('bulk-update/', StudentBulkUpdateView.as_view(), name='student-bulk-update'),
    
    # Individual student operations (must be last to avoid conflicts)
    # Now returns combined data by default
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
  # Field update operations
    path('<int:pk>/update/', StudentFieldUpdateView.as_view(), name='student-field-update'),
    path('<int:pk>/update-address/', StudentAddressFieldUpdateView.as_view(), name='student-address-field-update'),
]