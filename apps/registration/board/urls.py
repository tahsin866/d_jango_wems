from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('boards/', views.board_list, name='board-list'),
    path('boards/options/', views.board_options, name='board-options'),
    path('boards/<int:pk>/', views.board_detail, name='board-detail'),
]