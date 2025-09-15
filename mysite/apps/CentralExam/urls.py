from django.urls import path
from .views import (
    ExamSetupCreateView,
    ExamSetupListView,
    ExamSetupDetailView,
    ExamSetupUpdateView,
    ExamSetupDeleteView
)

urlpatterns = [
    # Create (POST)
    path('exam-setups/', ExamSetupCreateView.as_view(), name='exam_setup_create'),
    # List (GET)
    path('exam-setups/list/', ExamSetupListView.as_view(), name='exam_setup_list'),
    # Detail (GET)
    path('exam-setups/<int:exam_id>/', ExamSetupDetailView.as_view(), name='exam_setup_detail'),
    # Update (PUT)
    path('exam-setups/<int:exam_id>/update/', ExamSetupUpdateView.as_view(), name='exam_setup_update'),
    # Delete (DELETE)
    path('exam-setups/<int:exam_id>/delete/', ExamSetupDeleteView.as_view(), name='exam_setup_delete'),
]