from django.http import JsonResponse
from django.contrib.auth.models import User
from .decorators import admin_required, madrasa_required

@admin_required
def admin_dashboard_api(request):
    return JsonResponse({'message': 'Admin Dashboard Data', 'user_type': 'admin'})

@madrasa_required
def madrasa_dashboard_api(request):
    return JsonResponse({'message': 'Madrasa Dashboard Data', 'user_type': 'madrasa'})

def users_api(request):
    users = User.objects.all().values('id', 'username', 'email')
    return JsonResponse(list(users), safe=False)
