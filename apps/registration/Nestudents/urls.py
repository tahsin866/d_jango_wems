from django.urls import path
from .views import NewStudentRegistrationView

urlpatterns = [
    path('register/', NewStudentRegistrationView.as_view(), name='newstudent-register'),
]
