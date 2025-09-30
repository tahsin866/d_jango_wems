from django.urls import path, include

urlpatterns = [
    path('oldstudent/', include('apps.admin.registration.OldStudent.urls')),
]
