from django.urls import path
from .views import (
    ExamSetupCreateView,
    ExamSetupListView,
    ExamSetupDetailView,
    ExamSetupUpdateView,
    ExamSetupDeleteView,
    ExamFeeBulkCreateView,
    ExamFeeUpdateView,
    ExamFeeDetailView,
    ExamFeeListBySetupView,
    LatestExamSetupAPIView,   # ✅ নতুন ভিউ ইম্পোর্ট করুন
)

urlpatterns = [
    path('exam-setups/', ExamSetupCreateView.as_view(), name='exam_setup_create'),
    path('exam-setups/list/', ExamSetupListView.as_view(), name='exam_setup_list'),
    path('exam-setups/<int:exam_id>/', ExamSetupDetailView.as_view(), name='exam_setup_detail'),
    path('exam-setups/<int:exam_id>/update/', ExamSetupUpdateView.as_view(), name='exam_setup_update'),
    path('exam-setups/<int:exam_id>/delete/', ExamSetupDeleteView.as_view(), name='exam_setup_delete'),
    path('exam-setups/latest/', LatestExamSetupAPIView.as_view(), name='exam_setup_latest'),  # ✅ নতুন URL
    path('exam-fees/bulk-create/', ExamFeeBulkCreateView.as_view(), name='exam-fee-bulk-create'),
    path('exam-fees/<int:fee_id>/update/', ExamFeeUpdateView.as_view(), name='exam-fee-update'),
    path('exam-fees/<int:fee_id>/', ExamFeeDetailView.as_view(), name='exam-fee-detail'),
    path('exam-fees/by-setup/', ExamFeeListBySetupView.as_view(), name='exam-fee-list-by-setup'),
]