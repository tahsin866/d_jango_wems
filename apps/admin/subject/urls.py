from django.urls import path
from .views import (
    MarhalaWithCountsView, 
    MarhalaListView, 
    MarhalaSubjectListView,
    MarhalaSubjectCreateView,
    MarhalaWithSubjectsCreateView,
    MarhalaDetailView,
    MarhalaUpdateView,
    MarhalaDeleteView,
    SubjectSettingsListView,
    SubjectSettingsCreateView,
    SubjectSettingsDetailView,
    SubjectSettingsUpdateView,
    SubjectSettingsDeleteView,
    GetSubjectDataView,
    UpdateSubjectSettingView,

)

app_name = 'subject'

urlpatterns = [
    # মারহালা সম্পর্কিত URLs
    path('marhalas/', MarhalaListView.as_view(), name='marhala-list'),
    path('marhalas/with-counts/', MarhalaWithCountsView.as_view(), name='marhala-with-counts'),
    path('marhalas/create-with-subjects/', MarhalaWithSubjectsCreateView.as_view(), name='marhala-create-with-subjects'),
    path('marhalas/<int:marhala_id>/', MarhalaDetailView.as_view(), name='marhala-detail'),
    path('marhalas/<int:marhala_id>/update/', MarhalaUpdateView.as_view(), name='marhala-update'),
    path('marhalas/<int:marhala_id>/delete/', MarhalaDeleteView.as_view(), name='marhala-delete'),

    # সাবজেক্ট সম্পর্কিত URLs
    path('subjects/', MarhalaSubjectListView.as_view(), name='subject-list'),
    path('subjects/create/', MarhalaSubjectCreateView.as_view(), name='subject-create'),

    # সাবজেক্ট সেটিংস সম্পর্কিত URLs
    path('subject-settings/', SubjectSettingsListView.as_view(), name='subject-settings-list'),
    path('subject-settings/create/', SubjectSettingsCreateView.as_view(), name='subject-settings-create'),
    path('subject-settings/<int:settings_id>/', SubjectSettingsDetailView.as_view(), name='subject-settings-detail'),
    path('subject-settings/<int:settings_id>/update/', SubjectSettingsUpdateView.as_view(), name='subject-settings-update'),
    path('subject-settings/<int:settings_id>/delete/', SubjectSettingsDeleteView.as_view(), name='subject-settings-delete'),

    # নতুন Laravel-style endpoints
    path('marhala/<int:marhala_id>/subjects/', GetSubjectDataView.as_view(), name='get-subject-data'),
    path('subject-settings/<int:settings_id>/update-setting/', UpdateSubjectSettingView.as_view(), name='update-subject-setting'),

    # Exam fees by setup

]