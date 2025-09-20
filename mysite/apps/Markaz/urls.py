from django.urls import path
from .views import MadrashaSelectByElhaq

urlpatterns = [
    path('search-madrasa/', MadrashaSelectByElhaq.as_view(), name='search-madrasa'),
]
