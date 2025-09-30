from rest_framework.views import APIView
from rest_framework.response import Response
from .models import student_basic
from rest_framework.permissions import AllowAny

class YearsListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        year_pairs = student_basic.objects.values('year', 'hijri_year').distinct().order_by('-year')
        formatted_years = [
            f"{y['hijri_year']} হিজরি / {y['year']} ঈসাব্দ" for y in year_pairs if y['hijri_year'] and y['year']
        ]
        return Response(formatted_years)
