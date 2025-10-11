"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_dashboard_api, madrasa_dashboard_api
from .sidebar_api import get_sidebar_data, test_menu_data, clear_sidebar_cache, clear_department_sidebar_cache, get_user_department_info, get_user_type_config
from apps.users.auth_views import SecureSigninView, SecureLogoutView, get_user_profile, validate_route_access

urlpatterns = [
    # Authentication URLs
    path('api/auth/', include('apps.users.urls')),  # Main auth API endpoints
    
    # Legacy Authentication URLs (for backward compatibility)
    path('auth/signin/', SecureSigninView.as_view(), name='secure_signin'),
    path('auth/logout/', SecureLogoutView.as_view(), name='secure_logout'),
    path('auth/profile/', get_user_profile, name='user_profile'),
    path('auth/validate-route-access/', validate_route_access, name='validate_route_access'),

    # User management URLs
    path('users/', include('apps.users.urls')),
    
    # School URLs
    path('school/', include('apps.school.urls')),
    
    # Subject APIs
    path('api/', include('apps.admin.subject.urls')),

    # CentralExam APIs
    path('api/central-exam/', include('apps.admin.CentralExam.urls')),

    # Department APIs
    path('api/admin/departments/', include('apps.admin.department.urls')),

    # Dashboard APIs
    path('api/admin/dashboard/', admin_dashboard_api),
    path('api/madrasa/dashboard/', madrasa_dashboard_api),
    path('api/sidebar/', get_sidebar_data),
    path('api/test-menu/', test_menu_data),
    path('api/clear-sidebar-cache/', clear_sidebar_cache),
    path('api/clear-department-cache/', clear_department_sidebar_cache),
    path('api/user-department-info/', get_user_department_info),
    path('api/user-type-config/', get_user_type_config),
    # Markaz APIs
    path('api/markaz/', include('apps.Markaz.urls')),

    # Registration Overview API
    path('api/admin/registration/overview/', include('apps.registration.overview.urls')),
    path('api/admin/registration/', include('apps.registration.urls')),

    # Registration StudentList API
    path('api/registration/', include('apps.registration.StudentList.urls')),

    # Madrasha List API
    path('api/admin/madrasha/', include('apps.admin.madrasha.urls')),

    # Markaz List API
    path('api/admin/markaz/', include('apps.admin.markaz.urls')),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
