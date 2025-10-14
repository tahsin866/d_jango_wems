# apps/admin/madrasha/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
import hashlib

from apps.school.models import School
from apps.school.serializers import SchoolListSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Division, District, Thana
from .serializers import DivisionSerializer, DistrictSerializer, ThanaSerializer
from django.shortcuts import get_object_or_404

class MadrashaListView(APIView):
    permission_classes = [AllowAny]

    def get_cache_key(self, page, page_size):
        """Generate cache key for specific page"""
        return f"{settings.CACHE_MADRASHA_PAGE}:{page}:{page_size}"

    def get_total_count_cache_key(self):
        """Generate cache key for total count"""
        return settings.CACHE_MADRASHA_COUNT

    def get(self, request):
        # Pagination params
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            page_size = int(request.GET.get('page_size', 10))
        except ValueError:
            page_size = 10

        # Generate cache keys
        page_cache_key = self.get_cache_key(page, page_size)
        total_count_cache_key = self.get_total_count_cache_key()

        # Try to get cached data first
        cached_data = cache.get(page_cache_key)
        cached_total = cache.get(total_count_cache_key)

        if cached_data is not None and cached_total is not None:
            # Return cached data
            return Response({
                'results': cached_data,
                'total': cached_total,
                'page': page,
                'page_size': page_size,
                'cached': True
            })

        # If not in cache, fetch from database
        offset = (page - 1) * page_size
        limit = offset + page_size

        # Get total count (cache it separately)
        queryset = School.objects.all()

        # Apply any filters if present
        did_filter = request.GET.get('did')
        if did_filter:
            try:
                did_value = int(did_filter)
                queryset = queryset.filter(did=did_value)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        # Apply district filter if present
        des_id_filter = request.GET.get('des_id')
        if des_id_filter:
            try:
                des_id_value = int(des_id_filter)
                queryset = queryset.filter(des_id=des_id_value)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        # Apply thana filter if present
        tid_filter = request.GET.get('tid')
        if tid_filter:
            try:
                tid_value = int(tid_filter)
                queryset = queryset.filter(tid=tid_value)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        total = queryset.count()

        # Get paginated data
        schools = queryset[offset:limit]
        serializer = SchoolListSerializer(schools, many=True)

        # Cache the results
        cache.set(page_cache_key, serializer.data, settings.CACHE_TIMEOUT_MEDIUM)
        cache.set(total_count_cache_key, total, settings.CACHE_TIMEOUT_LONG)

        return Response({
            'results': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'cached': False
        })

    @staticmethod
    def clear_cache():
        """Clear all madrasha-related cache"""
        from django.core.cache import cache
        from django.conf import settings

        # Clear total count cache
        cache.delete(settings.CACHE_MADRASHA_COUNT)

        # Clear all paginated cache
        for page in range(1, 100):
            for page_size in [10, 25, 50, 100]:
                cache_key = f"{settings.CACHE_MADRASHA_PAGE}:{page}:{page_size}"
                cache.delete(cache_key)


class MadrashaCacheManagementView(APIView):
    """API view to manage madrasha cache"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Clear madrasha cache"""
        try:
            MadrashaListView.clear_cache()
            return Response({
                'message': 'Madrasha cache cleared successfully',
                'status': 'success'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f'Error clearing cache: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Get cache status information"""
        try:
            # Get some cache statistics
            total_count_cache_key = settings.CACHE_MADRASHA_COUNT
            cached_total = cache.get(total_count_cache_key)

            # Check some common page caches
            page_1_cache_key = f"{settings.CACHE_MADRASHA_PAGE}:1:10"
            cached_page_1 = cache.get(page_1_cache_key)

            return Response({
                'cache_backend': 'redis' if 'redis' in str(cache._cache) else 'memory',
                'total_count_cached': cached_total is not None,
                'page_1_cached': cached_page_1 is not None,
                'cached_total_count': cached_total if cached_total is not None else 0,
                'cache_keys': {
                    'total_count': total_count_cache_key,
                    'page_1': page_1_cache_key
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f'Error getting cache status: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DivisionListView(APIView):
    """API to get all divisions"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # dname ফিল্ড দিয়ে অর্ডার করুন
            divisions = Division.objects.all().order_by('division')
            serializer = DivisionSerializer(divisions, many=True)
            return Response({
                'results': serializer.data,
                'total': divisions.count()
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to fetch divisions'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DistrictListView(APIView):
    """API to get districts by division ID"""
    permission_classes = [AllowAny]

    def get(self, request):
        did = request.GET.get('did')
        try:
            if did:
                # Division টেবিলের id ফিল্ড দিয়ে ফিল্টার করুন
                districts = District.objects.filter(division__id=did).order_by('district')
            else:
                districts = District.objects.all().order_by('district')

            serializer = DistrictSerializer(districts, many=True)
            return Response({
                'results': serializer.data,
                'total': districts.count(),
                'did': did
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to fetch districts'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThanaListView(APIView):
    """API to get thanas by district ID"""
    permission_classes = [AllowAny]

    def get(self, request):
        district_id = request.GET.get('district_id')
        try:
            if district_id:
                # District টেবিলের desid ফিল্ড দিয়ে ফিল্টার করুন
                thanas = Thana.objects.filter(district__desid=district_id).order_by('thana')
            else:
                thanas = Thana.objects.all().order_by('thana')

            serializer = ThanaSerializer(thanas, many=True)
            return Response({
                'results': serializer.data,
                'total': thanas.count(),
                'district_id': district_id
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to fetch thanas'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MadrashaStatusUpdateView(APIView):
    """Update a school's active/inactive status (1=active, 0=inactive)."""
    permission_classes = [AllowAny]

    def post(self, request, pk: int):
        try:
            school = get_object_or_404(School, pk=pk)
            new_status = request.data.get('status', None)
            if new_status is None:
                return Response({'message': 'status is required (0 or 1)'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                new_status_int = int(new_status)
                if new_status_int not in (0, 1):
                    raise ValueError()
            except Exception:
                return Response({'message': 'Invalid status value. Must be 0 or 1.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update and save (status is a string field in the database)
            school.status = str(new_status_int)
            school.save(update_fields=['status'])

            # Clear cache so list reflects latest
            MadrashaListView.clear_cache()

            return Response({'message': 'Status updated', 'id': school.id, 'status': school.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to update status: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)