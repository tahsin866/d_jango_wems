from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.cache import cache as django_cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import School
from .serializers import SchoolCheckSerializer
import random
import string
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import uuid
import hashlib
from datetime import datetime, timedelta

def decrypt_aes_gcm(ciphertext_b64, iv_b64, key_b64):
    """Decrypt AES-GCM encrypted data"""
    try:
        # Decode from base64
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        key = base64.b64decode(key_b64)
        
        # Decrypt
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

class MadrashaCheckView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        # Get AES key from environment or settings
        aes_key = os.getenv('AES_KEY', 'YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWE')  # Replace with actual key
        
        # Check if data is encrypted (has IV fields)
        if 'elhaqno_iv' in request.data and 'mobile_iv' in request.data:
            # Decrypt encrypted data
            elhaqno = decrypt_aes_gcm(
                request.data.get('elhaqno', ''),
                request.data.get('elhaqno_iv', ''),
                aes_key
            )
            mobile = decrypt_aes_gcm(
                request.data.get('mobile', ''),
                request.data.get('mobile_iv', ''),
                aes_key
            )
            
            if not elhaqno or not mobile:
                return Response({'detail': 'ডেটা ডিক্রিপ্ট করতে সমস্যা হয়েছে!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Use plain text data
            elhaqno = request.data.get('elhaqno', '').strip()
            mobile = request.data.get('mobile', '').strip()
        
        if not elhaqno or not mobile:
            return Response({'detail': 'ইলহাক নম্বর এবং মোবাইল নম্বর প্রয়োজন!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug: Print received data
        print(f"Received - elhaqno: '{elhaqno}', mobile: '{mobile}'")
        
        # Create cache key for this search
        cache_key = f"school_search_{hashlib.md5(f'{elhaqno}_{mobile}'.encode()).hexdigest()}"
        
        # Try to get from cache first
        cached_school = django_cache.get(cache_key)
        if cached_school:
            school = cached_school
            print("School data retrieved from cache")
        else:
            # Check if school exists with optimized query (use select_related if needed)
            try:
                # Use exact match with database index optimization
                school = School.objects.filter(
                    elhaqno=elhaqno, 
                    mobile=mobile
                ).only('id', 'elhaqno', 'mobile', 'mname', 'village', 'post').first()
                
                if not school:
                    # Fallback: try case insensitive match
                    school = School.objects.filter(
                        elhaqno__iexact=elhaqno, 
                        mobile__iexact=mobile
                    ).only('id', 'elhaqno', 'mobile', 'mname', 'village', 'post').first()
                    
                if not school:
                    return Response({
                        'detail': 'ইলহাক নম্বর বা মোবাইল নম্বর ভুল!',
                        'debug': f"Searched for elhaqno: '{elhaqno}', mobile: '{mobile}'"
                    }, status=status.HTTP_404_NOT_FOUND)
                
                # Cache the school data for 5 minutes
                django_cache.set(cache_key, school, 300)
                print("School data cached for future requests")
                    
            except Exception as e:
                return Response({
                    'detail': 'ডাটাবেস ইরোর!',
                    'debug': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Generate custom registration code
        custom_code = 'SC-' + ''.join(random.choices(string.digits, k=6))
        
        # Generate temporary signup token (valid for 10 minutes)
        signup_token = str(uuid.uuid4())
        token_expiry = datetime.now() + timedelta(minutes=10)
        
        # Store token in session/cache (for simplicity using session here)
        # In production, use Redis or database
        from django.core.cache import cache
        cache.set(f'signup_token_{signup_token}', {
            'school_id': school.id,
            'elhaqno': school.elhaqno,
            'mobile': school.mobile,
            'expires_at': token_expiry.isoformat()
        }, 600)  # 10 minutes
        
        # Prepare response data with session info
        data = SchoolCheckSerializer(school).data
        data['registration_code'] = custom_code
        
        # Create response with redirect URL and session data
        response_data = {
            'redirect': f'/signup?token={signup_token}',  # Include token in URL
            'session': {
                'madrasha_name': school.mname,
                'post': school.post,
                'village': school.village,
                'registration_code': custom_code,
                'elhaqno': school.elhaqno,
                'mobile': school.mobile
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class ValidateSignupTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({'valid': False, 'detail': 'টোকেন প্রয়োজন!'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.core.cache import cache
        token_data = cache.get(f'signup_token_{token}')
        
        if not token_data:
            return Response({'valid': False, 'detail': 'টোকেন অবৈধ বা মেয়াদ শেষ!'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check expiry
        from datetime import datetime
        expires_at = datetime.fromisoformat(token_data['expires_at'])
        if datetime.now() > expires_at:
            cache.delete(f'signup_token_{token}')
            return Response({'valid': False, 'detail': 'টোকেনের মেয়াদ শেষ!'}, status=status.HTTP_410_GONE)
        
        # Get school data
        try:
            school = School.objects.get(id=token_data['school_id'])
            data = SchoolCheckSerializer(school).data
            return Response({'valid': True, 'school_data': data}, status=status.HTTP_200_OK)
        except School.DoesNotExist:
            return Response({'valid': False, 'detail': 'স্কুল ডেটা পাওয়া যায়নি!'}, status=status.HTTP_404_NOT_FOUND)
