from django.urls import path
from .views import MadrashaSelectByElhaq, MarkazApplicationCreateView
from .markaz_table import MarkazApplicationListView, MarkazApplicationDetailView
from mysite.apps.Markaz.markaz_Edit import MarkazApplicationFullDetailView, MarkazApplicationEditView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

urlpatterns = [
    path('search-madrasa/', MadrashaSelectByElhaq.as_view(), name='search-madrasa'),
    path('apply/', MarkazApplicationCreateView.as_view(), name='markaz-apply'),
    path('table/', MarkazApplicationListView.as_view(), name='markaz-table'),
    path('table/<int:pk>/', MarkazApplicationDetailView.as_view(), name='markaz-table-detail'),
    path('full-detail/<int:pk>/', MarkazApplicationFullDetailView.as_view(), name='markaz-full-detail'),
    path('edit/<int:pk>/', MarkazApplicationEditView.as_view(), name='markaz-edit'),
]
