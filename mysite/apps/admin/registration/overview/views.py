from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import RegistrationOverview
from .serializers import RegistrationOverviewSerializer

class RegistrationOverviewListView(generics.ListAPIView):
    serializer_class = RegistrationOverviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Redis cache setup
        from django.core.cache import cache
        exam_setup_id = self.request.query_params.get('exam_setup_id')
        cache_key = f'registration_overview_{exam_setup_id or "all"}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            # Return cached queryset (list of dicts)
            # We need to convert dicts to model instances for serializer, so skip and use cached response in list route
            # Here, just return empty queryset, actual data will be returned in list()
            return RegistrationOverview.objects.none()
        queryset = RegistrationOverview.objects.select_related('exam_setup', 'marhala').all()
        if exam_setup_id:
            queryset = queryset.filter(exam_setup_id=exam_setup_id)
        return queryset

    def list(self, request, *args, **kwargs):
        from django.core.cache import cache
        exam_setup_id = self.request.query_params.get('exam_setup_id')
        cache_key = f'registration_overview_{exam_setup_id or "all"}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return self.get_response_from_cache(cached_data)
        response = super().list(request, *args, **kwargs)
        # Cache the serialized data for 1 hour
        cache.set(cache_key, response.data, timeout=3600)
        return response

    def get_response_from_cache(self, cached_data):
        from rest_framework.response import Response
        return Response(cached_data)
