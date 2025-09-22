from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import RegistrationOverview
from .serializers import RegistrationOverviewSerializer

class RegistrationOverviewListView(generics.ListAPIView):
    queryset = RegistrationOverview.objects.select_related('exam_setup', 'marhala').all()
    serializer_class = RegistrationOverviewSerializer
    permission_classes = [AllowAny]
