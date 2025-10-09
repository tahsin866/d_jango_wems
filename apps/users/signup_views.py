from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
import jwt  # PyJWT package
import datetime
from django.conf import settings
from .serializers import UserRegistrationSerializer

class UserSignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle user registration with madrasha information"""
        print("Received signup data:", request.data)
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.save()
                user = result['user']
                user_info = result['user_info']
                user_type_created = result['user_type_created']
                
                # Log creation
                print(f"User created: {user.name} (ID: {user.id})")
                print(f"UserType {'created' if user_type_created else 'found'}: {user.user_type.name}")
                print(f"UserInformation created with madrasha_id: {user_info.madrasha_id}")

                # Set session data for automatic login
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_type'] = user.user_type.name
                request.session['user_email'] = user.email

                # Generate JWT token for frontend authentication
                token_payload = {
                    'user_id': user.id,
                    'user_name': user.name,
                    'user_type': user.user_type.name,
                    'email': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                    'iat': datetime.datetime.utcnow()
                }

                # Use a simple secret key (should be in settings)
                secret_key = getattr(settings, 'SECRET_KEY', 'your-secret-key')
                access_token = jwt.encode(token_payload, secret_key, algorithm='HS256')

                response_data = {
                    'success': True,
                    'message': 'রেজিস্ট্রেশন সফল হয়েছে!',
                    'access_token': access_token,  # Add JWT token
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                        'user_type': user.user_type.name,
                        'madrasha_id': user_info.madrasha_id,
                        'custom_code': user_info.custom_code,
                    },
                    'redirect': '/dashboard'  # Redirect to dashboard after successful registration
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Error during user creation: {str(e)}")
                return Response({
                    'success': False,
                    'detail': 'রেজিস্ট্রেশনে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।',
                    'debug': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Validation errors:", serializer.errors)
            return Response({
                'success': False,
                'detail': 'ফর্মে ত্রুটি রয়েছে।',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class UserSignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle user registration with madrasha information"""
        print("Received signup data:", request.data)
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.save()
                user = result['user']
                user_info = result['user_info']
                user_type_created = result['user_type_created']
                
                # Log creation
                print(f"User created: {user.name} (ID: {user.id})")
                print(f"UserType {'created' if user_type_created else 'found'}: {user.user_type.name}")

                print(f"UserInformation created with madrasha_id: {user_info.madrasha_id}")

                # madrasha_id আপডেট school_id দিয়ে
                from apps.school.models import School
                school = School.objects.filter(school_id=user_info.madrasha_id).first()
                if school:
                    user_info.madrasha_id = school.school_id  # schools টেবিলের school_id বসবে user_information টেবিলের madrasha_id-তে
                    user_info.save()

                # Set session data for automatic login
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_type'] = user.user_type.name
                request.session['user_email'] = user.email

                # Generate JWT token for frontend authentication
                token_payload = {
                    'user_id': user.id,
                    'user_name': user.name,
                    'user_type': user.user_type.name,
                    'email': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                    'iat': datetime.datetime.utcnow()
                }

                # Use a simple secret key (should be in settings)
                secret_key = getattr(settings, 'SECRET_KEY', 'your-secret-key')
                access_token = jwt.encode(token_payload, secret_key, algorithm='HS256')

                response_data = {
                    'success': True,
                    'message': 'রেজিস্ট্রেশন সফল হয়েছে!',
                    'access_token': access_token,  # Add JWT token
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                        'user_type': user.user_type.name,
                        'madrasha_id': user_info.madrasha_id,
                        'custom_code': user_info.custom_code,
                    },
                    'redirect': '/dashboard'  # Redirect to dashboard after successful registration
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Error during user creation: {str(e)}")
                return Response({
                    'success': False,
                    'detail': 'রেজিস্ট্রেশনে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।',
                    'debug': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Validation errors:", serializer.errors)
            return Response({
                'success': False,
                'detail': 'ফর্মে ত্রুটি রয়েছে।',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
