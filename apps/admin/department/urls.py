from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department-list'),
    path('user-types/', views.UserTypeListView.as_view(), name='user-type-list'),
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('menus/', views.MenuListView.as_view(), name='menu-list'),
    path('permissions/', views.PermissionListView.as_view(), name='permission-list'),
    path('modules/<int:department_id>/', views.get_modules_by_department, name='modules-by-department'),
    path('menus/<int:module_id>/', views.get_menus_by_module, name='menus-by-module'),
    path('name/<int:department_id>/', views.get_department_name, name='department-name'),
    # Commented out user permissions URLs as UserMenuPermission table doesn't exist
    # path('user-permissions/<int:user_id>/', views.get_user_permissions, name='user-permissions'),
    # path('user-permissions/<int:user_id>/save/', views.save_user_permissions, name='save-user-permissions'),
]