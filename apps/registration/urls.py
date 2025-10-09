from django.urls import path, include

urlpatterns = [
path('oldstudent/', include('apps.registration.OldStudent.urls')),
]
    