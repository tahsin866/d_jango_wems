# mysite/apps/Markaz/views.py

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment
from .serializers import MarkazApplicationSerializer, MainMadrasaInfoSerializer, AssociatedMadrasaSerializer, AttachmentSerializer
from rest_framework.permissions import AllowAny

class MarkazApplicationEditView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse JSON strings from FormData
        def parse_json_field(field_name):
            field_value = request.data.get(field_name)
            if isinstance(field_value, str):
                try:
                    return json.loads(field_value)
                except json.JSONDecodeError:
                    return {}
            return field_value or {}
        
        try:
            with transaction.atomic():
                # Parse JSON fields
                markaz_app_data = parse_json_field('markaz_application')
                main_madrasa_info_data = parse_json_field('main_madrasa_info')
                associated_madrasas_data = parse_json_field('associated_madrasas')
                deleted_madrasa_ids = parse_json_field('deleted_madrasa_ids')
                attachments_data = parse_json_field('attachments')

                # Update MarkazApplication
                try:
                    markaz_app = MarkazApplication.objects.get(id=pk)
                except MarkazApplication.DoesNotExist:
                    return Response({'success': False, 'error': 'MarkazApplication not found.'}, status=status.HTTP_404_NOT_FOUND)
                
                markaz_app_serializer = MarkazApplicationSerializer(markaz_app, data=markaz_app_data, partial=True)
                markaz_app_serializer.is_valid(raise_exception=True)
                markaz_app_serializer.save()

                # Update MainMadrasaInfo
                main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
                if main_madrasa:
                    main_madrasa_serializer = MainMadrasaInfoSerializer(main_madrasa, data=main_madrasa_info_data, partial=True)
                    main_madrasa_serializer.is_valid(raise_exception=True)
                    main_madrasa_serializer.save()

                # Delete removed associated madrasas
                for del_id in deleted_madrasa_ids:
                    AssociatedMadrasa.objects.filter(id=del_id, markaz_application_id=pk).delete()

                # Update or create AssociatedMadrasas
                for madrasa_data in associated_madrasas_data:
                    assoc_id = madrasa_data.get('id')
                    # Remove extra fields not in model
                    madrasa_data.pop('madrasa_name', None)
                    madrasa_data.pop('elhaqno', None)
                    if assoc_id:
                        # Update existing
                        assoc_madrasa = AssociatedMadrasa.objects.filter(id=assoc_id, markaz_application_id=pk).first()
                        if assoc_madrasa:
                            # Handle file uploads
                            if f'noc_file_{assoc_id}' in request.FILES:
                                madrasa_data['noc_file_path'] = request.FILES[f'noc_file_{assoc_id}']
                            if f'resolution_file_{assoc_id}' in request.FILES:
                                madrasa_data['resolution_file_path'] = request.FILES[f'resolution_file_{assoc_id}']
                            
                            assoc_madrasa_serializer = AssociatedMadrasaSerializer(assoc_madrasa, data=madrasa_data, partial=True)
                            assoc_madrasa_serializer.is_valid(raise_exception=True)
                            assoc_madrasa_serializer.save()
                    else:
                        # Create new
                        noc_file = madrasa_data.pop('noc_file', None)
                        resolution_file = madrasa_data.pop('resolution_file', None)
                        
                        new_madrasa = AssociatedMadrasa.objects.create(
                            markaz_application_id=pk,
                            **madrasa_data
                        )
                        
                        if noc_file:
                            new_madrasa.noc_file_path = noc_file
                        if resolution_file:
                            new_madrasa.resolution_file_path = resolution_file
                        new_madrasa.save()

                # Update Attachments
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

class MarkazApplicationFullDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch the MarkazApplication instance
            markaz_app = MarkazApplication.objects.get(id=pk)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'MarkazApplication not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data
        markaz_app_serializer = MarkazApplicationSerializer(markaz_app)
        
        # Fetch related data
        main_madrasa_info = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
        associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=pk)
        attachments = Attachment.objects.filter(markaz_application_id=pk)
        
        # Serialize related data
        main_madrasa_info_serializer = MainMadrasaInfoSerializer(main_madrasa_info) if main_madrasa_info else None
        associated_madrasas_serializer = AssociatedMadrasaSerializer(associated_madrasas, many=True)
        attachments_serializer = AttachmentSerializer(attachments, many=True)

        # Per-class counts for main madrasa
        main_class_counts = {}
        if main_madrasa_info:
            main_class_counts = {
                'ফযীলত': main_madrasa_info.fazilat or 0,
                'সানাবিয়া উলইয়া': main_madrasa_info.sanabiya_ulya or 0,
                'সানাবিয়া': main_madrasa_info.sanabiya or 0,
                'মুতাওয়াসসিতা': main_madrasa_info.mutawassita or 0,
                'ইবতেদাইয়্যাহ': main_madrasa_info.ibtedaiyyah or 0,
                'হিফজুল কোরান': main_madrasa_info.hifzul_quran or 0,
                'কিরাআত': main_madrasa_info.qirat or 0,
            }
        # Per-class counts for associated madrasas (total)
        associated_class_counts = {
            'ফযীলত': 0,
            'সানাবিয়া উলইয়া': 0,
            'সানাবিয়া': 0,
            'মুতাওয়াসসিতা': 0,
            'ইবতেদাইয়্যাহ': 0,
            'হিফজুল কোরান': 0,
            'কিরাআত': 0,
        }
        for assoc in associated_madrasas:
            associated_class_counts['ফযীলত'] += assoc.fazilat or 0
            associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
            associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
            associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
            associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
            associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
            associated_class_counts['কিরাআত'] += assoc.qirat or 0
        # Combine all data into a single response
        response_data = {
            'markaz_application': markaz_app_serializer.data,
            'main_madrasa_info': main_madrasa_info_serializer.data if main_madrasa_info_serializer else {},
            'main_class_counts': main_class_counts,
            'associated_madrasas': associated_madrasas_serializer.data,
            'associated_class_counts': associated_class_counts,
            'attachments': attachments_serializer.data
        }
        return Response({'success': True, 'data': response_data}, status=status.HTTP_200_OK)