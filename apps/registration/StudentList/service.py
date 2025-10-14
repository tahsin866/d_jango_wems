import redis
import json
from django.db import connection
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import urlparse
from .models import StudentBasic
from .serializers import StudentBasicListSerializer, StudentBasicSerializer
from apps.users.models import UserInformation

def get_redis_connection():
    """Get Redis connection from Django settings"""
    try:
        redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
        parsed_url = urlparse(redis_url)
        return redis.Redis(
            host=parsed_url.hostname,
            port=parsed_url.port,
            db=int(parsed_url.path.lstrip('/')) if parsed_url.path else 0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
    except Exception as e:
        print(f"Redis connection error: {e}")
        return None

def dict_hash(d):
    """Deterministic hash for dicts used in cache keys"""
    return hash(json.dumps(d, sort_keys=True)) if d else 0

def get_student_list(user_id=None, filters=None, page=1, page_size=10):
    """
    Get paginated student list with filters
    Filter by user's madrasha_id if user_id is provided
    """
    r = get_redis_connection()
    cache_key = f"student_list_{user_id}_{page}_{page_size}_{dict_hash(filters)}"

    try:
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")

    queryset = StudentBasic.objects.all()

    if user_id:
        try:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if user_info and user_info.madrasha_id:
                queryset = queryset.filter(madrasha_id=user_info.madrasha_id)
            else:
                queryset = queryset.none()
        except Exception as e:
            print(f"User filtering error: {e}")
            queryset = queryset.none()

    if filters:
        if filters.get('search'):
            search_term = filters['search']
            queryset = queryset.filter(
                Q(student_name_bn__icontains=search_term) |
                Q(father_name_bn__icontains=search_term) |
                Q(reg_no__icontains=search_term)
            )
        for field in ['marhala_id', 'exam_id', 'madrasha_id', 'students_type', 'status', 'year']:
            if filters.get(field):
                queryset = queryset.filter(**{field: filters[field]})

    queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    serializer = StudentBasicListSerializer(page_obj.object_list, many=True)

    result = {
        'students': serializer.data,
        'pagination': {
            'current_page': page,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'page_size': page_size,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        },
        'filters_applied': filters or {}
    }

    try:
        if r:
            r.setex(cache_key, 300, json.dumps(result, default=str))
    except Exception as e:
        print(f"Redis set error: {e}")

    return result

def get_student_detail(student_id, user_id=None):
    """
    Get detailed information for a single student
    Verify user has access to this student's data
    """
    r = get_redis_connection()
    cache_key = f"student_detail_{student_id}_{user_id}"

    try:
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")

    try:
        student = StudentBasic.objects.get(id=student_id)
        if user_id:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if not user_info or not user_info.madrasha_id or student.madrasha_id != user_info.madrasha_id:
                raise PermissionError("User cannot access this student's data")
        serializer = StudentBasicSerializer(student)
        result = serializer.data

        try:
            if r:
                r.setex(cache_key, 600, json.dumps(result, default=str))
        except Exception as e:
            print(f"Redis set error: {e}")

        return result

    except StudentBasic.DoesNotExist:
        return None
    except PermissionError as e:
        return {'error': str(e)}

def clear_student_caches():
    """Clear all student-related caches"""
    r = get_redis_connection()
    if r:
        try:
            patterns = [
                "student_list_*",
                "student_statistics*"
            ]
            for pattern in patterns:
                keys = r.keys(pattern)
                if keys:
                    r.delete(*keys)
        except Exception as e:
            print(f"Redis cache clear error: {e}")

def clear_student_detail_cache(student_id):
    """Clear cache for specific student detail"""
    r = get_redis_connection()
    if r:
        try:
            cache_keys = [
                f"student_detail_{student_id}_None",
                f"student_detail_combined_{student_id}_None"
            ]
            for cache_key in cache_keys:
                r.delete(cache_key)
            all_keys = r.keys(f"*student_detail*{student_id}*")
            if all_keys:
                r.delete(*all_keys)
        except Exception as e:
            print(f"Redis cache clear error: {e}")

def get_student_detail_combined(student_id, user_id=None):
    """
    Get combined student information from both student_basic and student_adresss tables
    """
    r = get_redis_connection()
    cache_key = f"student_detail_combined_{student_id}_{user_id}"

    try:
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")

    try:
        student = StudentBasic.objects.get(id=student_id)
        if user_id:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if not user_info or not user_info.madrasha_id or student.madrasha_id != user_info.madrasha_id:
                raise PermissionError("User cannot access this student's data")
        serializer = StudentBasicSerializer(student)
        result = serializer.data.copy()
        try:
            from apps.registration.OldStudent.models import student_adresss
            address_data = student_adresss.objects.filter(student_id=student_id).first()
            address_fields = [
                'division', 'district', 'thana', 'post_office', 'passport_photo',
                'birth_certificate_no', 'birth_certificate_photo', 'nid_no', 'nid_photo'
            ]
            for field in address_fields:
                result[field] = getattr(address_data, field, None) if address_data else None
        except Exception as e:
            print(f"Error fetching address data: {e}")
            for field in [
                'division', 'district', 'thana', 'post_office', 'passport_photo',
                'birth_certificate_no', 'birth_certificate_photo', 'nid_no', 'nid_photo'
            ]:
                result[field] = None
        try:
            if r:
                r.setex(cache_key, 600, json.dumps(result, default=str))
        except Exception as e:
            print(f"Redis set error: {e}")
        return result

    except StudentBasic.DoesNotExist:
        return None
    except PermissionError as e:
        return {'error': str(e)}

def update_student_field(student_id, field_name, field_value, user_id=None):
    """
    Update a single field in student_basic table
    """
    try:
        student = StudentBasic.objects.get(id=student_id)
        if user_id:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if not user_info or not user_info.madrasha_id or student.madrasha_id != user_info.madrasha_id:
                raise PermissionError("User cannot access this student's data")
        if not hasattr(student, field_name):
            return False, f"Invalid field name: {field_name}"
        setattr(student, field_name, field_value)
        if user_id:
            student.updated_by = user_id
        student.save()
        clear_student_caches()
        clear_student_detail_cache(student_id)
        return True, "Field updated successfully"
    except StudentBasic.DoesNotExist:
        return False, "Student not found"
    except Exception as e:
        print(f"Error updating field: {e}")
        return False, str(e)

def update_student_address_field(student_id, field_name, field_value, user_id=None):
    """
    Update a single field in student_adresss table
    """
    try:
        student = StudentBasic.objects.get(id=student_id)
        if user_id:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if not user_info or not user_info.madrasha_id or student.madrasha_id != user_info.madrasha_id:
                raise PermissionError("User cannot access this student's data")
        from apps.registration.OldStudent.models import student_adresss
        address_obj, created = student_adresss.objects.get_or_create(
            student_id=student_id,
            defaults={field_name: field_value}
        )
        if not hasattr(address_obj, field_name):
            return False, f"Invalid address field name: {field_name}"
        if not created:
            setattr(address_obj, field_name, field_value)
            address_obj.save()
        clear_student_caches()
        clear_student_detail_cache(student_id)
        return True, "Address field updated successfully"
    except StudentBasic.DoesNotExist:
        return False, "Student not found"
    except Exception as e:
        print(f"Error updating address field: {e}")
        return False, str(e)


def create_student(student_data, user_id=None):
    """
    Create a new student record
    """
    from .serializers import StudentBasicCreateUpdateSerializer
    from apps.users.models import UserInformation
    from apps.Markaz.models import MadrashaUnderCenter

    if user_id:
        student_data['created_by'] = user_id

    if user_id:
        try:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if user_info and user_info.madrasha_id:
                if not student_data.get('madrasha_id'):
                    student_data['madrasha_id'] = user_info.madrasha_id
                if not student_data.get('markaz_id'):
                    mapping = MadrashaUnderCenter.objects.filter(child_madrasha_id=str(user_info.madrasha_id)).first()
                    if mapping and mapping.parent_madrasha_id:
                        student_data['markaz_id'] = int(mapping.parent_madrasha_id) if str(mapping.parent_madrasha_id).isdigit() else None
        except Exception as e:
            print(f"[create_student] markaz auto-mapping failed: {e}")

    serializer = StudentBasicCreateUpdateSerializer(data=student_data)
    if serializer.is_valid():
        student = serializer.save()
        clear_student_caches()
        return student, None
    else:
        return None, serializer.errors


def update_student(student_id, student_data, user_id=None):
    """
    Update an existing student record
    """
    from .serializers import StudentBasicCreateUpdateSerializer

    try:
        student = StudentBasic.objects.get(id=student_id)

        if user_id:
            student_data['updated_by'] = user_id

        serializer = StudentBasicCreateUpdateSerializer(student, data=student_data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            clear_student_caches()
            clear_student_detail_cache(student_id)
            return student, None
        else:
            return None, serializer.errors
    except StudentBasic.DoesNotExist:
        return None, {'error': 'Student not found'}


def delete_student(student_id, user_id=None):
    """
    Delete a student record
    """
    try:
        student = StudentBasic.objects.get(id=student_id)
        student_name = student.student_name_bn
        student.delete()

        clear_student_caches()
        clear_student_detail_cache(student_id)

        return True, f"Student {student_name} deleted successfully"
    except StudentBasic.DoesNotExist:
        return False, "Student not found"


def get_student_statistics(user_id=None):
    """
    Get basic statistics about students
    Filter by user's madrasha_id if user_id is provided
    """
    r = get_redis_connection()
    cache_key = f"student_statistics_{user_id}"

    try:
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")

    from django.db import connection
    sql_query = """
        SELECT
            COUNT(*) as total_students,
            COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_students,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_students,
            COUNT(CASE WHEN status = 'submitted' THEN 1 END) as submitted_students,
            COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned_students,
            COUNT(DISTINCT exam_id) as total_exams,
            COUNT(DISTINCT madrasha_id) as total_madrashas,
            COUNT(DISTINCT marhala_id) as total_marhalas
        FROM student_basic
    """

    query_params = []

    if user_id:
        try:
            user_info = UserInformation.objects.filter(user_id=user_id).first()
            if user_info and user_info.madrasha_id:
                sql_query += " WHERE madrasha_id = %s"
                query_params.append(user_info.madrasha_id)
            else:
                return {
                    'total_students': 0,
                    'approved_students': 0,
                    'pending_students': 0,
                    'submitted_students': 0,
                    'returned_students': 0,
                    'total_exams': 0,
                    'total_madrashas': 0,
                    'total_marhalas': 0
                }
        except Exception as e:
            print(f"User filtering error in statistics: {e}")
            return {
                'total_students': 0,
                'approved_students': 0,
                'pending_students': 0,
                'submitted_students': 0,
                'returned_students': 0,
                'total_exams': 0,
                'total_madrashas': 0,
                'total_marhalas': 0
            }

    with connection.cursor() as cursor:
        cursor.execute(sql_query, query_params)

        row = cursor.fetchone()
        if row:
            stats = {
                'total_students': row[0],
                'approved_students': row[1],
                'pending_students': row[2],
                'submitted_students': row[3],
                'returned_students': row[4],
                'total_exams': row[5],
                'total_madrashas': row[6],
                'total_marhalas': row[7]
            }

            try:
                if r:
                    r.setex(cache_key, 1800, json.dumps(stats))
            except Exception as e:
                print(f"Redis set error: {e}")

            return stats

    return {
        'total_students': 0,
        'approved_students': 0,
        'pending_students': 0,
        'submitted_students': 0,
        'returned_students': 0,
        'total_exams': 0,
        'total_madrashas': 0,
        'total_marhalas': 0
    }


def bulk_update_students(student_updates, user_id=None):
    """
    Bulk update multiple students
    """
    success_count = 0
    error_count = 0
    errors = []

    for student_data in student_updates:
        student_id = student_data.get('id')
        if not student_id:
            error_count += 1
            errors.append({"error": "Student ID is required"})
            continue

        student, error = update_student(student_id, student_data, user_id)
        if student:
            success_count += 1
        else:
            error_count += 1
            errors.append({"id": student_id, "error": error})

    return {
        'success_count': success_count,
        'error_count': error_count,
        'errors': errors
    }