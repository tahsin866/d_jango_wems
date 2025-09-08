from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])
def get_sidebar_data(request):
    """Get modules and menus for sidebar - formatted for frontend structure"""
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
        
        return Response({'sidebar_data': sidebar_modules})

@api_view(['GET'])
@permission_classes([AllowAny])
def test_menu_data(request):
    """Test endpoint to check menu data"""
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
        
        return Response({'test_menus': menus})
