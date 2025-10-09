# apps/admin/markaz/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
import hashlib

from apps.Markaz.models import MadrashaCenter
from apps.school.models import School
from .serializers import MadrashaCenterListSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.admin.madrasha.models import Division, District, Thana
from apps.admin.madrasha.serializers import DivisionSerializer, DistrictSerializer, ThanaSerializer
from django.shortcuts import get_object_or_404

class MarkazCenterListView(APIView):
    """List Madrasha Centers with joined School data"""
    permission_classes = [AllowAny]

    def get_cache_key(self, page, page_size):
        """Generate cache key for specific page"""
        return f"{settings.CACHE_MARKAZ_PAGE}:{page}:{page_size}"

    def get_total_count_cache_key(self):
        """Generate cache key for total count"""
        return settings.CACHE_MARKAZ_COUNT

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

        # Get total count
        queryset = MadrashaCenter.objects.all()

        # Apply any filters if present
        did_filter = request.GET.get('did')
        if did_filter:
            try:
                did_value = int(did_filter)
                # Filter by school's division through madrasha_id -> school_id
                school_ids = School.objects.filter(did=did_value).values_list('school_id', flat=True)
                queryset = queryset.filter(madrasha_id__in=school_ids)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        # Apply district filter if present
        des_id_filter = request.GET.get('des_id')
        if des_id_filter:
            try:
                des_id_value = int(des_id_filter)
                # Filter by school's district through madrasha_id -> school_id
                school_ids = School.objects.filter(des_id=des_id_value).values_list('school_id', flat=True)
                queryset = queryset.filter(madrasha_id__in=school_ids)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        # Apply thana filter if present
        tid_filter = request.GET.get('tid')
        if tid_filter:
            try:
                tid_value = int(tid_filter)
                # Filter by school's thana through madrasha_id -> school_id
                school_ids = School.objects.filter(tid=tid_value).values_list('school_id', flat=True)
                queryset = queryset.filter(madrasha_id__in=school_ids)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        # Apply center filter if present
        center_id_filter = request.GET.get('center_id')
        if center_id_filter:
            try:
                center_id_value = int(center_id_filter)
                queryset = queryset.filter(center_id=center_id_value)
            except (ValueError, TypeError):
                pass  # Invalid filter value, ignore

        total = queryset.count()

        # Get paginated data
        madrasha_centers = queryset[offset:limit]
        serializer = MadrashaCenterListSerializer(madrasha_centers, many=True)

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
        """Clear all markaz-related cache"""
        from django.core.cache import cache
        from django.conf import settings

        # Clear total count cache
        cache.delete(settings.CACHE_MARKAZ_COUNT)

        # Clear all paginated cache
        for page in range(1, 100):
            for page_size in [10, 25, 50, 100]:
                cache_key = f"{settings.CACHE_MARKAZ_PAGE}:{page}:{page_size}"
                cache.delete(cache_key)


class MarkazCacheManagementView(APIView):
    """API view to manage markaz cache"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Clear markaz cache"""
        try:
            MarkazCenterListView.clear_cache()
            return Response({
                'message': 'Markaz cache cleared successfully',
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
            total_count_cache_key = settings.CACHE_MARKAZ_COUNT
            cached_total = cache.get(total_count_cache_key)

            # Check some common page caches
            page_1_cache_key = f"{settings.CACHE_MARKAZ_PAGE}:1:10"
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


class MarkazStatusUpdateView(APIView):
    """Update a school's active/inactive status (1=active, 0=inactive) for markaz madrashas."""
    permission_classes = [AllowAny]

    def post(self, request, pk: int):
        """
        Update the status of a school associated with a madrasha center.
        pk here is the MadrashaCenter id, but we update the corresponding School status.
        """
        try:
            # Get the madrasha center
            madrasha_center = get_object_or_404(MadrashaCenter, pk=pk)

            # Find the corresponding school
            if not madrasha_center.madrasha_id:
                return Response({'message': 'Madrasha center has no associated madrasha_id'}, status=status.HTTP_400_BAD_REQUEST)

            school = School.objects.filter(school_id=madrasha_center.madrasha_id).first()
            if not school:
                school = School.objects.filter(id=madrasha_center.madrasha_id).first()

            if not school:
                return Response({'message': 'Associated school not found'}, status=status.HTTP_404_NOT_FOUND)

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
            MarkazCenterListView.clear_cache()

            return Response({'message': 'Status updated', 'id': school.id, 'status': school.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to update status: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Reuse the same division, district, and thana views from madrasha
class DivisionListView(APIView):
    """API to get all divisions"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
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


class CenterListView(APIView):
    """API to get all centers"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            from apps.Markaz.models import Center
            # Include both actual centers from database and center types (1, 2, 3)
            center_types = [
                {'id': 1, 'name': 'দারসিয়াত', 'code': 'DARSIYAT'},
                {'id': 2, 'name': 'হিফজ', 'code': 'HIFZ'},
                {'id': 3, 'name': 'কিরাআত', 'code': 'QIRAT'}
            ]

            # Get centers from database if they exist
            try:
                db_centers = Center.objects.all().order_by('name')
                db_center_data = [{'id': center.id, 'name': center.name, 'code': center.code} for center in db_centers]
                center_types.extend(db_center_data)
            except:
                # If Center table doesn't exist or has no data, just use center types
                pass

            return Response({
                'results': center_types,
                'total': len(center_types)
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to fetch centers'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarkazStatisticsView(APIView):
    """API to get markaz statistics from database tables"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            from apps.Markaz.models import MadrashaCenter
            from apps.school.models import School

            # 1. Total Markaz Madrasha (count from madrasha_centers table)
            total_markaz = MadrashaCenter.objects.count()

            # 2. Get all madrasha_ids from madrasha_centers
            markaz_madrasha_ids = MadrashaCenter.objects.values_list('madrasha_id', flat=True)

            # 3. Count male and female madrashas from schools table where mtype=1 and mtype=0
            # Connect through madrasha_id (madrasha_centers) to school_id (schools)
            male_count = School.objects.filter(
                school_id__in=markaz_madrasha_ids,
                mtype=1
            ).count()

            female_count = School.objects.filter(
                school_id__in=markaz_madrasha_ids,
                mtype=0
            ).count()

            # 4. Count active madrashas (status='1') from schools table connected to madrasha_centers
            active_count = School.objects.filter(
                school_id__in=markaz_madrasha_ids,
                status='1'
            ).count()

            return Response({
                'total_markaz': total_markaz,
                'male_count': male_count,
                'female_count': female_count,
                'active_count': active_count
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to fetch markaz statistics'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)