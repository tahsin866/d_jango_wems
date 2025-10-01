from django.urls import path
from .views import RegistrationOverviewListView

urlpatterns = [
    path('', RegistrationOverviewListView.as_view(), name='registration-overview-list'),
]
