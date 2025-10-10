from django.urls import path
from .views import (
    ModuleListAPIView, get_user_modules_menus, debug_session, test_modules
)
from .signup_views import UserSignupView
from .auth_views import (
    validate_route_access,
    validate_token,
    validate_session,
    check_session,
    SecureSigninView,
    SecureLogoutView,
    get_user_profile,
    create_login_history,   # <-- এইটা import করতে হবে!
)
from .profile_views import (
    update_user_profile, upload_profile_photo, get_profile_fallback
)

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

    # --- Add these for authentication ---
    path('auth/signin/', SecureSigninView.as_view(), name='secure_signin'),
    path('auth/logout/', SecureLogoutView.as_view(), name='secure_logout'),
    path('auth/profile/', get_user_profile, name='user_profile'),
    path('auth/validate/', validate_token, name='validate_token'),
    path('auth/validate-session/', validate_session, name='validate_session'),
    path('auth/check-session/', check_session, name='check_session'),

    # --- Add your login history API endpoint ---
    path('login-history/create/', create_login_history, name='create-login-history'),  # <--- এখানে যোগ করুন!
]