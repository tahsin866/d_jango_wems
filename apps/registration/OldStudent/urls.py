from django.urls import path
from .views import OldStudentSearchView
from .years_api import YearsListView

urlpatterns = [
    path('search/', OldStudentSearchView.as_view(), name='old-student-search'),
    path('years/', YearsListView.as_view(), name='years-list'),
    
]
