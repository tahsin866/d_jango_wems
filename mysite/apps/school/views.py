from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .service.services import madrasha_check_service, validate_signup_token_service

class MadrashaCheckView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        response_data, error_data, code = madrasha_check_service(request.data)
        if error_data:
            return Response(error_data, status=code)
        return Response(response_data, status=code)

class ValidateSignupTokenView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        data, code = validate_signup_token_service(token)
        return Response(data, status=code)