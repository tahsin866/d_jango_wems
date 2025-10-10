from django.urls import path
from .views import (
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentStatisticsView,
    StudentBulkUpdateView,
    StudentSearchView
)

urlpatterns = [
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
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]