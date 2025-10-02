from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from rest_framework.permissions import AllowAny

class YearsListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        years_list = Student.objects.values_list('years', flat=True).distinct().order_by('-years')
        formatted_years = [str(y) for y in years_list if y]
        return Response(formatted_years)
