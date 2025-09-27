from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment
from mysite.apps.Markaz.serializers import MarkazApplicationSerializer, MainMadrasaInfoSerializer, AssociatedMadrasaSerializer, AttachmentSerializer
from rest_framework.permissions import AllowAny

class MarkazApplicationEditView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        try:
            with transaction.atomic():
                # Update MarkazApplication
                markaz_app_data = data.get('markaz_application') or {}
                try:
                    markaz_app = MarkazApplication.objects.get(id=pk)
                except MarkazApplication.DoesNotExist:
                    return Response({'success': False, 'error': 'MarkazApplication not found.'}, status=status.HTTP_404_NOT_FOUND)
                markaz_app_serializer = MarkazApplicationSerializer(markaz_app, data=markaz_app_data, partial=True)
                markaz_app_serializer.is_valid(raise_exception=True)
                markaz_app_serializer.save()

                # Update MainMadrasaInfo
                main_madrasa_info_data = data.get('main_madrasa_info', {})
                main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
                if main_madrasa:
                    main_madrasa_serializer = MainMadrasaInfoSerializer(main_madrasa, data=main_madrasa_info_data, partial=True)
                    main_madrasa_serializer.is_valid(raise_exception=True)
                    main_madrasa_serializer.save()

                # Update AssociatedMadrasas
                associated_madrasas_data = data.get('associated_madrasas', [])
                for madrasa_data in associated_madrasas_data:
                    assoc_id = madrasa_data.get('id')
                    if assoc_id:
                        assoc_madrasa = AssociatedMadrasa.objects.filter(id=assoc_id, markaz_application_id=pk).first()
                        if assoc_madrasa:
                            assoc_madrasa_serializer = AssociatedMadrasaSerializer(assoc_madrasa, data=madrasa_data, partial=True)
                            assoc_madrasa_serializer.is_valid(raise_exception=True)
                            assoc_madrasa_serializer.save()

                # Update Attachments
                attachments_data = data.get('attachments', [])
                for attachment_data in attachments_data:
                    attach_id = attachment_data.get('id')
                    if attach_id:
                        attachment = Attachment.objects.filter(id=attach_id, markaz_application_id=pk).first()
                        if attachment:
                            attachment_serializer = AttachmentSerializer(attachment, data=attachment_data, partial=True)
                            attachment_serializer.is_valid(raise_exception=True)
                            attachment_serializer.save()

            return Response({'success': True, 'message': 'Updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
