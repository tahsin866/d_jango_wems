from django.urls import path
from .views import (
    MadrashaSelectByElhaq,
    MadrasaSearchAPIView,
    MarkazApplicationCreateView,
    MarkazApplicationListView,
    MarkazApplicationDetailView,
    MarkazApplicationFullDetailView,
    MarkazApplicationEditView,
)

urlpatterns = [
    path('search-madrasa/', MadrashaSelectByElhaq.as_view(), name='search-madrasa'),
    path('search-madrasa-cache/', MadrasaSearchAPIView.as_view(), name='search-madrasa-cache'),
    path('apply/', MarkazApplicationCreateView.as_view(), name='markaz-apply'),
    path('table/', MarkazApplicationListView.as_view(), name='markaz-table'),
    path('table/<int:pk>/', MarkazApplicationDetailView.as_view(), name='markaz-table-detail'),
    path('full-detail/<int:pk>/', MarkazApplicationFullDetailView.as_view(), name='markaz-full-detail'),
    path('edit/<int:pk>/', MarkazApplicationEditView.as_view(), name='markaz-edit'),
]