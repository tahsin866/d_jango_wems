from django.urls import path
from .views import (
    ExamSetupCreateView,
    ExamSetupListView,
    ExamSetupDetailView,
    ExamSetupUpdateView,
    ExamSetupDeleteView
)

urlpatterns = [
    # Laravel store_1 function এর মতো - POST request for creating exam setup
    path('exam-setups/', ExamSetupCreateView.as_view(), name='exam_setup_create'),
    
    # Other CRUD operations  
    path('exam-setups/list/', ExamSetupListView.as_view(), name='exam_setup_list'),
    path('exam-setups/<int:exam_id>/', ExamSetupDetailView.as_view(), name='exam_setup_detail'),
    path('exam-setups/<int:exam_id>/update/', ExamSetupUpdateView.as_view(), name='exam_setup_update'),
    path('exam-setups/<int:exam_id>/delete/', ExamSetupDeleteView.as_view(), name='exam_setup_delete'),
]