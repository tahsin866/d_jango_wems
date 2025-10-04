from django.urls import path
from .views import OldStudentSearchView, OldStudentRegistrationView
from .years_api import YearsListView

urlpatterns = [
    path('search/', OldStudentSearchView.as_view(), name='old-student-search'),
    path('years/', YearsListView.as_view(), name='years-list'),
    path('register/', OldStudentRegistrationView.as_view(), name='old-student-register'),
    
]
