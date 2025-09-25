from django.urls import path
from .views import ModuleListAPIView, get_user_modules_menus, debug_session, test_modules
from .signup_views import UserSignupView
from .auth_views import (
    validate_route_access,
)
from .profile_views import get_user_profile, update_user_profile, upload_profile_photo, get_profile_fallback

urlpatterns = [
    path('modules/', ModuleListAPIView.as_view(), name='module-list'),
    path('user-modules/', get_user_modules_menus, name='user-modules-menus'),
    path('debug-session/', debug_session, name='debug-session'),
    path('test-modules/', test_modules, name='test-modules'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('validate-route-access/', validate_route_access, name='validate-route-access'),
    path('profile/', get_user_profile, name='get-user-profile'),
    path('profile/update/', update_user_profile, name='update-user-profile'),
    path('profile/upload-photo/', upload_profile_photo, name='upload-profile-photo'),
    path('profile/fallback/', get_profile_fallback, name='get-profile-fallback'),
]