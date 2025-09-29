from django.urls import path, include

urlpatterns = [
    path('oldstudent/', include('mysite.apps.admin.registration.OldStudent.urls')),
]
