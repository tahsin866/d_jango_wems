from django.http import JsonResponse
from .decorators import admin_required, madrasa_required
from apps.registration.OldStudent.models import student_basic, student_results
from apps.users.models import User  # or the actual model names

@admin_required
def admin_dashboard_api(request):
    return JsonResponse({'message': 'Admin Dashboard Data', 'user_type': 'admin'})

@madrasa_required
def madrasa_dashboard_api(request):
    return JsonResponse({'message': 'Madrasa Dashboard Data', 'user_type': 'madrasa'})

def users_api(request):
    users = User.objects.all().values('id', 'username', 'email')
    return JsonResponse(list(users), safe=False)
