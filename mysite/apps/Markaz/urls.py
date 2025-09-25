from django.urls import path
from .views import MadrashaSelectByElhaq, MarkazApplicationCreateView

urlpatterns = [
    path('search-madrasa/', MadrashaSelectByElhaq.as_view(), name='search-madrasa'),
    path('apply/', MarkazApplicationCreateView.as_view(), name='markaz-apply'),
]
