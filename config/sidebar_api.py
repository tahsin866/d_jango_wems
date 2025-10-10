from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
from django.conf import settings


class SidebarCache:
    """Sidebar cache management class"""
    
    # Cache timeout constants (in seconds)
    CACHE_TIMEOUT_SHORT = 5 * 60        # 5 minutes
    CACHE_TIMEOUT_MEDIUM = 15 * 60      # 15 minutes  
    CACHE_TIMEOUT_LONG = 60 * 60        # 1 hour
    
    # Cache key templates
    SIDEBAR_DATA_KEY = f"{getattr(settings, 'CACHE_KEY_PREFIX', 'wems')}:sidebar:data"
    MODULES_KEY = f"{getattr(settings, 'CACHE_KEY_PREFIX', 'wems')}:sidebar:modules"
    MENUS_KEY = f"{getattr(settings, 'CACHE_KEY_PREFIX', 'wems')}:sidebar:menus"
    
    @staticmethod
    def set_cache(key, data, timeout=None):
        """Set cache with default timeout"""
        if timeout is None:
            timeout = SidebarCache.CACHE_TIMEOUT_LONG  # Sidebar data changes rarely
        return cache.set(key, data, timeout)
    
    @staticmethod
    def get_cache(key):
        """Get cache data"""
        return cache.get(key)
    
    @staticmethod
    def delete_cache(key):
        """Delete cache data"""
        return cache.delete(key)
    
    @staticmethod
    def invalidate_sidebar_cache():
        """Invalidate all sidebar related cache"""
        SidebarCache.delete_cache(SidebarCache.SIDEBAR_DATA_KEY)
        SidebarCache.delete_cache(SidebarCache.MODULES_KEY)
        SidebarCache.delete_cache(SidebarCache.MENUS_KEY)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sidebar_data(request):
    """Get modules and menus for sidebar - filtered by user's department"""

    # Get user ID and department ID from multiple sources (priority order)
    user_id = None
    department_id = None
    
    # 1. Try to get from query parameters (highest priority for flexibility)
    if request.GET.get('user_id'):
        user_id = request.GET.get('user_id')
    if request.GET.get('department_id'):
        department_id = request.GET.get('department_id')
    
    # 2. Try to get from session (if not in query params)
    if not user_id and hasattr(request, 'session'):
        user_id = request.session.get('user_id')
    if not department_id and hasattr(request, 'session'):
        department_id = request.session.get('department_id')
    
    # 3. Try from authenticated user (lowest priority)
    if not user_id and hasattr(request, 'user') and request.user.is_authenticated:
        user_id = request.user.id

    print(f"[Sidebar API] user_id: {user_id}, department_id: {department_id} (from {'query' if request.GET.get('department_id') else 'session'})")

    # If no user_id provided, return all modules (fallback behavior)
    if not user_id:
        print("[Sidebar API] No user_id found, returning all modules")
        return get_all_sidebar_data()

    # Try to get from cache first for this specific user/department
    cache_key = f"{SidebarCache.SIDEBAR_DATA_KEY}:user:{user_id}:dept:{department_id or 'none'}"
    cached_data = SidebarCache.get_cache(cache_key)

    if cached_data:
        print(f"[Sidebar API] Returning cached data for user {user_id}, dept {department_id}")
        return Response({
            'sidebar_data': cached_data,
            'cached': True,
            'user_id': user_id,
            'department_id': department_id,
            'message': 'সাইডবার ডেটা ক্যাশ থেকে লোড হয়েছে'
        })

    with connection.cursor() as cursor:
        # Get user's department_id if not provided
        if not department_id:
            cursor.execute("""
                SELECT u.department_id, d.name as department_name
                FROM users u
                LEFT JOIN departments d ON u.department_id = d.id
                WHERE u.id = %s
            """, [user_id])

            user_result = cursor.fetchone()
            if not user_result:
                print(f"[Sidebar API] User {user_id} not found")
                return Response({
                    'error': 'User not found',
                    'sidebar_data': []
                }, status=404)

            department_id, department_name = user_result
        else:
            # Get department name
            cursor.execute("""
                SELECT name FROM departments WHERE id = %s
            """, [department_id])
            dept_result = cursor.fetchone()
            department_name = dept_result[0] if dept_result else 'Unknown'

        print(f"[Sidebar API] Loading sidebar for user {user_id}, department {department_id} ({department_name})")

        # If user has no department, return empty sidebar
        if not department_id:
            print(f"[Sidebar API] User {user_id} has no department, returning empty sidebar")
            return Response({
                'sidebar_data': [],
                'user_id': user_id,
                'department_id': None,
                'department_name': 'No Department',
                'message': 'ব্যবহারকারীর কোনো বিভাগ নেই'
            })

        # Get modules for this department (matching department_id, NOT including NULL)
        # Changed from "OR m.department_id IS NULL" to only match exact department
        cursor.execute("""
            SELECT m.id, m.name, m.description, m.icon, m.department_id
            FROM modules m
            WHERE m.department_id = %s
            ORDER BY m.id
        """, [department_id])

        sidebar_modules = []
        module_count = 0
        total_fetched = 0
        for module_row in cursor.fetchall():
            total_fetched += 1
            module_id, module_name, module_description, module_icon, mod_dept_id = module_row
            module_count += 1

            print(f"[Sidebar API] Processing Module {module_id}: {module_name} (Dept: {mod_dept_id})")

            # Get menus for this module
            cursor.execute("""
                SELECT mn.id, mn.name, mn.description, mn.href, mn.icon
                FROM menus mn
                WHERE mn.module_id = %s
                ORDER BY mn.id
            """, [module_id])

            menu_items = []
            for menu_row in cursor.fetchall():
                menu_id, menu_name, menu_description, menu_href, menu_icon = menu_row
                menu_items.append({
                    'label': menu_name,
                    'href': menu_href or '#',
                    'icon': menu_icon or 'DocsIcon'
                })

            if menu_items:  # Only add modules that have menus
                sidebar_modules.append({
                    'label': module_name,
                    'icon': module_icon or 'SettingsIcon',
                    'items': menu_items
                })

        print(f"[Sidebar API] Total modules fetched from DB: {total_fetched}, With menus: {len(sidebar_modules)}")

        # Cache the result for this user's department
        SidebarCache.set_cache(cache_key, sidebar_modules, SidebarCache.CACHE_TIMEOUT_LONG)

        return Response({
            'sidebar_data': sidebar_modules,
            'cached': False,
            'user_id': user_id,
            'department_id': department_id,
            'department_name': department_name,
            'total_modules': len(sidebar_modules),
            'message': f'সাইডবার ডেটা ডেটাবেস থেকে লোড হয়েছে ({department_name} বিভাগ)'
        })


def get_all_sidebar_data():
    """Get all modules and menus (fallback function)"""

    # Try to get from cache first
    cached_data = SidebarCache.get_cache(SidebarCache.SIDEBAR_DATA_KEY)

    if cached_data:
        return Response({
            'sidebar_data': cached_data,
            'cached': True,
            'message': 'সাইডবার ডেটা ক্যাশ থেকে লোড হয়েছে'
        })

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.id, m.name, m.description, m.icon
            FROM modules m
            ORDER BY m.id
        """)

        sidebar_modules = []
        for module_row in cursor.fetchall():
            module_id, module_name, module_description, module_icon = module_row

            # Get menus for this module
            cursor.execute("""
                SELECT mn.id, mn.name, mn.description, mn.href, mn.icon
                FROM menus mn
                WHERE mn.module_id = %s
                ORDER BY mn.id
            """, [module_id])

            menu_items = []
            for menu_row in cursor.fetchall():
                menu_id, menu_name, menu_description, menu_href, menu_icon = menu_row
                menu_items.append({
                    'label': menu_name,
                    'href': menu_href or '#',
                    'icon': menu_icon or 'DocsIcon'
                })

            if menu_items:  # Only add modules that have menus
                sidebar_modules.append({
                    'label': module_name,
                    'icon': module_icon or 'SettingsIcon',
                    'items': menu_items
                })

        # Cache the result for long duration since sidebar data rarely changes
        SidebarCache.set_cache(SidebarCache.SIDEBAR_DATA_KEY, sidebar_modules, SidebarCache.CACHE_TIMEOUT_LONG)

        return Response({
            'sidebar_data': sidebar_modules,
            'cached': False,
            'message': 'সাইডবার ডেটা ডেটাবেস থেকে লোড হয়েছে'
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def test_menu_data(request):
    """Test endpoint to check menu data"""
    
    # Try to get from cache first
    cached_data = SidebarCache.get_cache(SidebarCache.MENUS_KEY)
    
    if cached_data:
        return Response({
            'test_menus': cached_data,
            'cached': True,
            'message': 'টেস্ট মেনু ডেটা ক্যাশ থেকে লোড হয়েছে'
        })
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT mn.id, mn.name, mn.icon, mn.href
            FROM menus mn
            LIMIT 10
        """)
        
        menus = []
        for row in cursor.fetchall():
            menu_id, menu_name, menu_icon, menu_href = row
            menus.append({
                'id': menu_id,
                'name': menu_name,
                'icon': menu_icon,
                'href': menu_href
            })
        
        # Cache the result
        SidebarCache.set_cache(SidebarCache.MENUS_KEY, menus, SidebarCache.CACHE_TIMEOUT_MEDIUM)
        
        return Response({
            'test_menus': menus,
            'cached': False,
            'message': 'টেস্ট মেনু ডেটা ডেটাবেস থেকে লোড হয়েছে'
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def clear_sidebar_cache(request):
    """Clear sidebar cache - useful for admin operations"""
    try:
        SidebarCache.invalidate_sidebar_cache()
        return Response({
            'success': True,
            'message': 'সাইডবার ক্যাশ সফলভাবে clear হয়েছে'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'ক্যাশ clear করতে সমস্যা: {str(e)}'
        }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def clear_department_sidebar_cache(request):
    """Clear department-specific sidebar cache"""
    try:
        user_id = request.data.get('user_id')
        if user_id:
            # Clear cache for specific user
            cache_key = f"{SidebarCache.SIDEBAR_DATA_KEY}:user:{user_id}"
            SidebarCache.delete_cache(cache_key)
            return Response({
                'success': True,
                'message': f'ইউজার {user_id} এর সাইডবার ক্যাশ সফলভাবে clear হয়েছে'
            })
        else:
            # Clear all sidebar cache
            SidebarCache.invalidate_sidebar_cache()
            return Response({
                'success': True,
                'message': 'সব সাইডবার ক্যাশ সফলভাবে clear হয়েছে'
            })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'ক্যাশ clear করতে সমস্যা: {str(e)}'
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_department_info(request):
    """Get current user's department information"""
    user_id = request.GET.get('user_id')

    # If no user_id provided, try to get from authenticated user
    if not user_id and hasattr(request, 'user') and request.user.is_authenticated:
        user_id = request.user.id

    if not user_id:
        return Response({
            'error': 'User ID required',
            'message': 'ইউজার ID প্রয়োজন'
        }, status=400)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.department_id, d.name as department_name
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = %s
        """, [user_id])

        user_result = cursor.fetchone()
        if not user_result:
            return Response({
                'error': 'User not found',
                'message': 'ইউজার পাওয়া যায়নি'
            }, status=404)

        user_id, user_name, user_email, department_id, department_name = user_result

        return Response({
            'user_id': user_id,
            'user_name': user_name,
            'user_email': user_email,
            'department_id': department_id,
            'department_name': department_name,
            'message': 'ইউজার তথ্য সফলভাবে পাওয়া গেছে'
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_type_config(request):
    """Get user type configuration for sidebar behavior"""
    user_type = request.GET.get('user_type', 'general')

    # Define different sidebar configurations based on user types
    user_configs = {
        'master_admin': {
            'can_access_all_modules': True,
            'cache_timeout': 300,  # 5 minutes
            'show_admin_tools': True
        },
        'department_manager': {
            'can_access_all_modules': False,
            'cache_timeout': 900,  # 15 minutes
            'show_admin_tools': False
        },
        'general': {
            'can_access_all_modules': False,
            'cache_timeout': 1800,  # 30 minutes
            'show_admin_tools': False
        }
    }

    config = user_configs.get(user_type, user_configs['general'])

    return Response({
        'user_type': user_type,
        'config': config,
        'message': f'{user_type} ইউজার কনফিগারেশন'
    })
