from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment
from mysite.apps.Markaz.serializers import MarkazApplicationSerializer, MainMadrasaInfoSerializer, AssociatedMadrasaSerializer, AttachmentSerializer
from rest_framework.permissions import AllowAny

class MarkazApplicationFullDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            markaz_app = MarkazApplication.objects.get(id=pk)
            markaz_app_data = MarkazApplicationSerializer(markaz_app).data
            main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
            main_madrasa_data = MainMadrasaInfoSerializer(main_madrasa).data if main_madrasa else None
            associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=pk)
            associated_madrasas_data = AssociatedMadrasaSerializer(associated_madrasas, many=True).data
            attachments = Attachment.objects.filter(markaz_application_id=pk)
            attachments_data = AttachmentSerializer(attachments, many=True).data
            return Response({
                'success': True,
                'data': {
                    'markaz_application': markaz_app_data,
                    'main_madrasa_info': main_madrasa_data,
                    'associated_madrasas': associated_madrasas_data,
                    'attachments': attachments_data
                }
            }, status=status.HTTP_200_OK)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
