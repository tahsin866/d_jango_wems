from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
import pytz

from mysite.apps.Markaz.models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa
from mysite.apps.school.models import School
from mysite.apps.CentralExam.models import ExamSetup

BN_MONTHS = [
    'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
    'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'
]

def format_bangla_date(dt):
    if not dt:
        return ''
    dt = dt.astimezone(pytz.timezone('Asia/Dhaka'))
    return f"{dt.day} {BN_MONTHS[dt.month - 1]}, {dt.year}"

class MarkazApplicationListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.user.id
        applications = MarkazApplication.objects.filter(user_id=user_id).order_by('-created_at')
        result = []
        for app in applications:
            # ... (your list code as before)
            # Main MadrasaInfo fetch
            main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=app.id).first()
            madrasa_id = main_madrasa.madrasa_id if main_madrasa else None
            madrasa_name = None
            main_total_students = 0
            if main_madrasa:
                main_total_students = sum([
                    main_madrasa.fazilat or 0,
                    main_madrasa.sanabiya_ulya or 0,
                    main_madrasa.sanabiya or 0,
                    main_madrasa.mutawassita or 0,
                    main_madrasa.ibtedaiyyah or 0,
                    main_madrasa.hifzul_quran or 0,
                    main_madrasa.qirat or 0,
                ])
                school = School.objects.filter(id=madrasa_id).first()
                madrasa_name = school.mname if school else None

            associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=app.id)
            associated_list = []
            associated_total_students = 0
            for assoc in associated_madrasas:
                assoc_madrasa_id = assoc.madrasa_id
                assoc_madrasa_name = None
                assoc_students = sum([
                    assoc.fazilat or 0,
                    assoc.sanabiya_ulya or 0,
                    assoc.sanabiya or 0,
                    assoc.mutawassita or 0,
                    assoc.ibtedaiyyah or 0,
                    assoc.hifzul_quran or 0,
                    assoc.qirat or 0,
                ])
                associated_total_students += assoc_students
                if assoc_madrasa_id:
                    school = School.objects.filter(id=assoc_madrasa_id).first()
                    assoc_madrasa_name = school.mname if school else None
                associated_list.append({
                    'id': assoc.id,
                    'madrasa_id': assoc_madrasa_id,
                    'madrasa_name': assoc_madrasa_name,
                    'total_students': assoc_students,
                })

            exam_name = None
            if app.exam_id:
                exam = ExamSetup.objects.filter(id=app.exam_id).first()
                if exam:
                    exam_name = exam.exam_name

            result.append({
                'id': app.id,
                'user_id': app.user_id,
                'markaz_type': app.markaz_type,
                'created_at': str(app.created_at),
                'exam_id': app.exam_id,
                'exam_name': exam_name,
                'status': app.status,
                'main_madrasa_id': madrasa_id,
                'main_madrasa_name': madrasa_name,
                'main_total_students': main_total_students,
                'associated_madrasas': associated_list,
                'associated_total_students': associated_total_students,
            })
        return Response({'success': True, 'data': result}, status=status.HTTP_200_OK)

class MarkazApplicationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            app = MarkazApplication.objects.get(id=pk)
            # Main MadrasaInfo fetch, Associated Madrasa fetch, Exam fetch (code same as above, just for one app)
            # ... (copy code from above for one instance)
            main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=app.id).first()
            madrasa_id = main_madrasa.madrasa_id if main_madrasa else None
            madrasa_name = None
            main_total_students = 0
            if main_madrasa:
                main_total_students = sum([
                    main_madrasa.fazilat or 0,
                    main_madrasa.sanabiya_ulya or 0,
                    main_madrasa.sanabiya or 0,
                    main_madrasa.mutawassita or 0,
                    main_madrasa.ibtedaiyyah or 0,
                    main_madrasa.hifzul_quran or 0,
                    main_madrasa.qirat or 0,
                ])
                school = School.objects.filter(id=madrasa_id).first()
                madrasa_name = school.mname if school else None

            associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=app.id)
            associated_list = []
            associated_total_students = 0
            for assoc in associated_madrasas:
                assoc_madrasa_id = assoc.madrasa_id
                assoc_madrasa_name = None
                assoc_students = sum([
                    assoc.fazilat or 0,
                    assoc.sanabiya_ulya or 0,
                    assoc.sanabiya or 0,
                    assoc.mutawassita or 0,
                    assoc.ibtedaiyyah or 0,
                    assoc.hifzul_quran or 0,
                    assoc.qirat or 0,
                ])
                associated_total_students += assoc_students
                if assoc_madrasa_id:
                    school = School.objects.filter(id=assoc_madrasa_id).first()
                    assoc_madrasa_name = school.mname if school else None
                associated_list.append({
                    'id': assoc.id,
                    'madrasa_id': assoc_madrasa_id,
                    'madrasa_name': assoc_madrasa_name,
                    'total_students': assoc_students,
                })

            exam_name = None
            if app.exam_id:
                exam = ExamSetup.objects.filter(id=app.exam_id).first()
                if exam:
                    exam_name = exam.exam_name

            result = {
                'id': app.id,
                'user_id': app.user_id,
                'markaz_type': app.markaz_type,
                'created_at': str(app.created_at),
                'exam_id': app.exam_id,
                'exam_name': exam_name,
                'status': app.status,
                'main_madrasa_id': madrasa_id,
                'main_madrasa_name': madrasa_name,
                'main_total_students': main_total_students,
                'associated_madrasas': associated_list,
                'associated_total_students': associated_total_students,
            }
            return Response({'success': True, 'data': result}, status=status.HTTP_200_OK)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            app = MarkazApplication.objects.get(id=pk)
            # Audit entry
            from mysite.apps.Markaz.models import MarkazApplicationAudit
            MarkazApplicationAudit.objects.create(
                markaz_application=app,
                action='delete',
                ip_address=request.META.get('REMOTE_ADDR'),
                status=app.status,
                printed=app.printed,
                created_at=timezone.now()
            )
            app.delete()
            return Response({'success': True, 'message': 'Deleted successfully.'}, status=status.HTTP_200_OK)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)