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
from .sidebar_api import get_sidebar_data, test_menu_data, clear_sidebar_cache
from .apps.users.auth_views import SecureSigninView, SecureLogoutView, get_user_profile, validate_route_access

urlpatterns = [
    # Secure Authentication URLs
    path('auth/signin/', SecureSigninView.as_view(), name='secure_signin'),
    path('auth/logout/', SecureLogoutView.as_view(), name='secure_logout'),
    path('auth/profile/', get_user_profile, name='user_profile'),
    path('auth/validate-route-access/', validate_route_access, name='validate_route_access'),
    
    # Other auth URLs
    path('auth/', include('mysite.apps.school.urls')),
    path('auth/', include('mysite.apps.users.urls')),  # Add users URLs
    
    # Subject APIs
    path('api/', include('mysite.apps.subject.urls')),
    
    # CentralExam APIs
    path('api/central-exam/', include('mysite.apps.CentralExam.urls')),
    path('users/', include('mysite.apps.users.urls')),  # <-- শুধু এভাবে include করুন!
    # Dashboard APIs
    path('api/admin/dashboard/', admin_dashboard_api),
    path('api/madrasa/dashboard/', madrasa_dashboard_api),
    path('api/sidebar/', get_sidebar_data),
    path('api/test-menu/', test_menu_data),
    path('api/clear-sidebar-cache/', clear_sidebar_cache),
    # Markaz APIs
    path('api/markaz/', include('mysite.apps.Markaz.urls')),

    # Registration Overview API
    path('api/admin/registration/overview/', include('mysite.apps.admin.registration.overview.urls')),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
