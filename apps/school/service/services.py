import random
import string
import base64
import os
import uuid
import hashlib
from datetime import datetime, timedelta

from django.core.cache import cache as django_cache
from ..models import School
from ..serializers import SchoolCheckSerializer
from ..cache import decrypt_aes_gcm

def madrasha_check_service(request_data):
    aes_key = os.getenv('AES_KEY', 'YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWE')
    if 'elhaqno_iv' in request_data and 'mobile_iv' in request_data:
        elhaqno = decrypt_aes_gcm(
            request_data.get('elhaqno', ''),
            request_data.get('elhaqno_iv', ''),
            aes_key
        )
        mobile = decrypt_aes_gcm(
            request_data.get('mobile', ''),
            request_data.get('mobile_iv', ''),
            aes_key
        )
        if not elhaqno or not mobile:
            return None, {'detail': 'ডেটা ডিক্রিপ্ট করতে সমস্যা হয়েছে!'}, 400
    else:
        elhaqno = request_data.get('elhaqno', '').strip()
        mobile = request_data.get('mobile', '').strip()
    if not elhaqno or not mobile:
        return None, {'detail': 'ইলহাক নম্বর এবং মোবাইল নম্বর প্রয়োজন!'}, 400
    cache_key = f"school_search_{hashlib.md5(f'{elhaqno}_{mobile}'.encode()).hexdigest()}"
    cached_school = django_cache.get(cache_key)
    school = cached_school
    if not school:
        try:
            school = School.objects.filter(
                elhaqno=elhaqno, mobile=mobile
            ).only('id', 'elhaqno', 'mobile', 'mname', 'village', 'post').first()
            if not school:
                school = School.objects.filter(
                    elhaqno__iexact=elhaqno, mobile__iexact=mobile
                ).only('id', 'elhaqno', 'mobile', 'mname', 'village', 'post').first()
            if not school:
                return None, {
                    'detail': 'ইলহাক নম্বর বা মোবাইল নম্বর ভুল!',
                    'debug': f"Searched for elhaqno: '{elhaqno}', mobile: '{mobile}'"
                }, 404
            django_cache.set(cache_key, school, 300)
        except Exception as e:
            return None, {'detail': 'ডাটাবেস ইরোর!', 'debug': str(e)}, 500
    custom_code = 'SC-' + ''.join(random.choices(string.digits, k=6))
    signup_token = str(uuid.uuid4())
    token_expiry = datetime.now() + timedelta(minutes=10)
    django_cache.set(f'signup_token_{signup_token}', {
        'school_id': school.school_id,
        'elhaqno': school.elhaqno,
        'mobile': school.mobile,
        'expires_at': token_expiry.isoformat()
    }, 600)
    data = SchoolCheckSerializer(school).data
    data['registration_code'] = custom_code
    response_data = {
        'redirect': f'/signup?token={signup_token}',
        'session': {
            'madrasha_name': school.mname,
            'post': school.post,
            'village': school.village,
            'registration_code': custom_code,
            'elhaqno': school.elhaqno,
            'mobile': school.mobile
        }
    }
    return response_data, None, 200

def validate_signup_token_service(token):
    if not token:
        return {'valid': False, 'detail': 'টোকেন প্রয়োজন!'}, 400
    token_data = django_cache.get(f'signup_token_{token}')
    if not token_data:
        return {'valid': False, 'detail': 'টোকেন অবৈধ বা মেয়াদ শেষ!'}, 404
    expires_at = datetime.fromisoformat(token_data['expires_at'])
    if datetime.now() > expires_at:
        django_cache.delete(f'signup_token_{token}')
        return {'valid': False, 'detail': 'টোকেনের মেয়াদ শেষ!'}, 410
    try:
        school = School.objects.get(school_id=token_data['school_id'])
        data = SchoolCheckSerializer(school).data
        return {'valid': True, 'school_data': data}, 200
    except School.DoesNotExist:
        return {'valid': False, 'detail': 'স্কুল ডেটা পাওয়া যায়নি!'}, 404