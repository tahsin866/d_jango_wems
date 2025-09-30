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
    """Get modules and menus for sidebar - formatted for frontend structure"""
    
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
                print(f"Menu: {menu_name}, Icon: {menu_icon}")  # Debug print
                menu_items.append({
                    'label': menu_name,
                    'href': menu_href or '#',
                    'icon': menu_icon or 'DocsIcon'
                })
            
            if menu_items:  # Only add modules that have menus
                sidebar_modules.append({
                    'label': module_name,
                    'icon': module_icon or 'SettingsIcon',  # Use module icon from database
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
