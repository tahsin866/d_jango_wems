from rest_framework.views import APIView
from rest_framework.response import Response
from .models import student_basic
from rest_framework.permissions import AllowAny

class YearsListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        years = student_basic.objects.values_list('year', flat=True).distinct().order_by('-year')
        return Response(list(years))
