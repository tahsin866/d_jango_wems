from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user_type = getattr(request, 'user_type', None) or request.session.get('user_type')
        if user_type != 'admin':
            return JsonResponse({'error': 'Admin access required'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def madrasa_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user_type = getattr(request, 'user_type', None) or request.session.get('user_type')
        if user_type != 'madrasa':
            return JsonResponse({'error': 'Madrasa access required'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def authenticated_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view
