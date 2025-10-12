from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.cache import cache
from apps.registration.OldStudent.models import student_basic, student_adresss, student_attachment
from apps.users.models import UserInformation
from apps.school.models import School
from apps.registration.board.models import Board
from .serializers import NewStudentSerializer
import random

BEFAQ_BOARD_NAME = 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ'

class NewStudentRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_user_madrasha_id(self, user_id):
        """user_information টেবিল থেকে user_id দিয়ে madrasha_id পাওয়া"""
        try:
            user_info = UserInformation.objects.get(user_id=user_id)
            return user_info.madrasha_id
        except UserInformation.DoesNotExist:
            return None
        except Exception as e:
            print(f"❌ user madrasha_id পেতে সমস্যা: {str(e)}")
            return None

    def get_auto_markaz_id(self, madrasha_id):
        """madrasha_under_centers থেকে markaz_id স্বয়ংক্রিয়ভাবে নির্ধারণ"""
        try:
            from apps.Markaz.models import MadrashaUnderCenter
            mapping = MadrashaUnderCenter.objects.filter(child_madrasha_id=str(madrasha_id)).first()
            if mapping and mapping.parent_madrasha_id:
                auto_markaz_id = int(mapping.parent_madrasha_id) if str(mapping.parent_madrasha_id).isdigit() else None
                print(f"✅ স্বয়ংক্রিয় markaz_id: {auto_markaz_id}")
                return auto_markaz_id
            else:
                print(f"⚠️ madrasha_id {madrasha_id} এর জন্য কোনো markaz mapping পাওয়া যায়নি")
                return None
        except Exception as e:
            print(f"❌ markaz_id স্বয়ংক্রিয়ভাবে নির্ধারণে সমস্যা: {e}")
            return None

    def get_auto_exam_id(self):
        """ExamSetup টেবিল থেকে বর্তমান বছরের exam_id পাওয়া"""
        try:
            from apps.admin.CentralExam.models import ExamSetup
            current_year = timezone.now().year

            # কৌশল ১: বর্তমান বছরের সাথে সঠিক মিল
            exam_setup = ExamSetup.objects.filter(
                english_year=str(current_year)
            ).first()

            # কৌশল ২: যদি সঠিক মিল না পাওয়া যায়, contains চেষ্টা করুন
            if not exam_setup:
                exam_setup = ExamSetup.objects.filter(
                    english_year__contains=str(current_year)
                ).first()

            # কৌশল ৩: এখনও যদি মিল না পাওয়া যায়, সর্বশেষটি নিন
            if not exam_setup:
                exam_setup = ExamSetup.objects.order_by('-created_at').first()

            exam_id = exam_setup.id if exam_setup else None
            print(f"✅ স্বয়ংক্রিয় exam_id: {exam_id}")
            return exam_id
        except Exception as e:
            print(f"❌ exam_id স্বয়ংক্রিয়ভাবে নির্ধারণে সমস্যা: {e}")
            return None

    def get_marhala_id_from_header(self, request):
        """
        হেডার থেকে marhala_id পাওয়ার উন্নত পদ্ধতি
        দুটি ভিন্ন ফরম্যাট সাপোর্ট করে:
        1. HTTP_X_MARHALA_ID (Django META format)
        2. X-Marhala-ID (Standard header format)
        """
        try:
            # প্রথমে Django META ফরম্যাট চেষ্টা করুন
            marhala_id = request.META.get('HTTP_X_MARHALA_ID')
            
            # যদি না পাওয়া যায়, তাহলে স্ট্যান্ডার্ড হেডার ফরম্যাট চেষ্টা করুন
            if not marhala_id:
                marhala_id = request.headers.get('X-Marhala-ID')
            
            # যদি এখনও না পাওয়া যায়, case-insensitive চেষ্টা করুন
            if not marhala_id:
                # সব হেডার খুঁজে বের করুন
                for header_name, header_value in request.headers.items():
                    if header_name.lower() == 'x-marhala-id':
                        marhala_id = header_value
                        break
            
            if not marhala_id:
                print(f"⚠️ হেডারে marhala_id পাওয়া যায়নি")
                print(f"📋 উপলব্ধ হেডার: {dict(request.headers)}")
                return None
                
            print(f"✅ হেডার থেকে marhala_id পাওয়া গেছে: {marhala_id}")
            
            # সংখ্যা কিনা যাচাই করুন
            if str(marhala_id).isdigit():
                return int(marhala_id)
            else:
                print(f"⚠️ marhala_id বৈধ সংখ্যা নয়: {marhala_id}")
                return None
                
        except Exception as e:
            print(f"❌ হেডার থেকে marhala_id পেতে সমস্যা: {e}")
            return None

    def get_cid_from_marhala_id(self, marhala_id):
        """marhala_id থেকে cid নির্ধারণের লজিক"""
        try:
            if not marhala_id:
                print(f"⚠️ cid নির্ধারণের জন্য marhala_id প্রদান করা হয়নি")
                return None

            marhala_id = int(marhala_id)
            
            # marhala_id → cid ম্যাপিং লজিক
            cid_mapping = {
                9: 2,   # দাখিল ৯ম শ্রেণী
                10: 3,  # দাখিল ১০ম শ্রেণী
                11: 4,  # আলিম ১ম বর্ষ
                12: 5,  # আলিম ২য় বর্ষ
                14: 6,  # ফাজিল ১ম বর্ষ
                15: 7,
                 16: 8,  # ফাজিল ২য় বর্ষ
            }
            
            cid = cid_mapping.get(marhala_id)
            
            if cid:
                print(f"✅ marhala_id {marhala_id} → cid {cid}")
                return cid
            else:
                print(f"⚠️ marhala_id {marhala_id} এর জন্য কোনো cid ম্যাপিং নেই")
                return None
                
        except Exception as e:
            print(f"❌ marhala_id থেকে cid পেতে সমস্যা: {e}")
            return None

    def get_srtype_from_user_madrasha(self, user_id):
        """user_information.madrasha_id দিয়ে schools টেবিল থেকে srtype (mtype) পাওয়া"""
        try:
            # প্রথমে user_information থেকে madrasha_id পান
            user_info = UserInformation.objects.get(user_id=user_id)
            madrasha_id = user_info.madrasha_id

            if madrasha_id:
                # এখন madrasha_id দিয়ে school রেকর্ড পান
                school = School.objects.filter(madrasha_id=madrasha_id).first()
                if school:
                    srtype = school.mtype
                    print(f"✅ schools টেবিল থেকে srtype (mtype): {srtype}")
                    return srtype
                else:
                    print(f"⚠️ madrasha_id {madrasha_id} এর জন্য কোনো school পাওয়া যায়নি")
                    return None
            else:
                print(f"⚠️ user_id {user_id} এর জন্য madrasha_id পাওয়া যায়নি")
                return None
        except UserInformation.DoesNotExist:
            print(f"⚠️ user_id {user_id} এর জন্য UserInformation পাওয়া যায়নি")
            return None
        except Exception as e:
            print(f"❌ user madrasha থেকে srtype পেতে সমস্যা: {e}")
            return None

    def get_board_id_from_board_table(self, board_name):
        """board টেবিল থেকে board_id পাওয়া"""
        try:
            if not board_name:
                print(f"⚠️ board_name প্রদান করা হয়নি")
                return None
                
            print(f"🔍 board_name খোঁজা হচ্ছে: '{board_name}'")
            
            # সঠিক মিলের জন্য চেষ্টা করুন
            board = Board.objects.filter(board_name=board_name).first()
            if board:
                board_id = board.id
                print(f"✅ board টেবিল থেকে board_id: {board_id}")
                return board_id
            
            # case-insensitive মিলের জন্য চেষ্টা করুন
            board = Board.objects.filter(board_name__iexact=board_name).first()
            if board:
                board_id = board.id
                print(f"✅ board টেবিল থেকে board_id (case-insensitive): {board_id}")
                return board_id
            
            # contains মিলের জন্য চেষ্টা করুন
            board = Board.objects.filter(board_name__icontains=board_name).first()
            if board:
                board_id = board.id
                print(f"✅ board টেবিল থেকে board_id (contains): {board_id}")
                return board_id
            
            print(f"⚠️ '{board_name}' নামে কোনো board পাওয়া যায়নি")
            return None
            
        except Exception as e:
            print(f"❌ board টেবিল থেকে board_id পেতে সমস্যা: {e}")
            return None

    def post(self, request):
        print("🚀 নতুন ছাত্র রেজিস্ট্রেশন API কল হয়েছে")
        print(f"📋 রিকোয়েস্ট হেডার: {dict(request.headers)}")
        print(f"📋 রিকোয়েস্ট ডেটা কী: {list(request.data.keys())}")

        serializer = NewStudentSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"❌ সিরিয়ালাইজার ত্রুটি: {serializer.errors}")
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        print(f"✅ ভ্যালিডেটেড ডেটা: {data}")

        # রিকোয়েস্ট থেকে user_id পান
        user_id = (request.data.get('user_id') or 
                  request.data.get('user') or 
                  (request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None))
        print(f"👤 ইউজার ID: {user_id}")

        # স্বয়ংক্রিয়ভাবে madrasha_id এবং markaz_id ডিটেক্ট করুন
        user_madrasha_id = None
        auto_markaz_id = None
        auto_exam_id = None

        if user_id:
            user_madrasha_id = self.get_user_madrasha_id(user_id)
            if user_madrasha_id:
                print(f"✅ user_information থেকে madrasha_id: {user_madrasha_id}")
                auto_markaz_id = self.get_auto_markaz_id(user_madrasha_id)
            else:
                print(f"⚠️ user_id {user_id} এর জন্য madrasha_id পাওয়া যায়নি")
                # ডিফল্ট ফলব্যাক ভ্যালু
                user_madrasha_id = 1
                auto_markaz_id = 1
        else:
            print("⚠️ রিকোয়েস্টে user_id প্রদান করা হয়নি - ডিফল্ট ভ্যালু ব্যবহার করা হচ্ছে")
            user_madrasha_id = 1
            auto_markaz_id = 1

        # ExamSetup টেবিল থেকে স্বয়ংক্রিয় exam_id ডিটেক্ট করুন
        auto_exam_id = self.get_auto_exam_id()

        # প্রয়োজনীয় ফিল্ডের জন্য বিশেষ লজিক প্রয়োগ করুন
        # ১. marhala_id -> হেডার থেকে পান
        header_marhala_id = self.get_marhala_id_from_header(request)
        final_marhala_id = header_marhala_id or data.get('marhala_id')
        print(f"🎯 চূড়ান্ত marhala_id: {final_marhala_id} (হেডার: {header_marhala_id}, ফর্ম: {data.get('marhala_id')})")

        # ২. cid -> marhala_id লজিক ভিত্তিক
        marhala_cid = self.get_cid_from_marhala_id(final_marhala_id)
        final_cid = marhala_cid or data.get('cid')
        print(f"🎯 চূড়ান্ত cid: {final_cid} (marhala_id থেকে: {marhala_cid}, ফর্ম: {data.get('cid')})")

        # ৩. srtype -> user_information.madrasha_id দিয়ে schools টেবিল থেকে mtype পান
        if user_id:
            header_srtype = self.get_srtype_from_user_madrasha(user_id)
            final_srtype = header_srtype or data.get('srtype')
            print(f"🎯 চূড়ান্ত srtype: {final_srtype} (ইউজার মাদ্রাসা থেকে: {header_srtype}, ফর্ম: {data.get('srtype')})")
        else:
            final_srtype = data.get('srtype')
            print(f"🎯 চূড়ান্ত srtype: {final_srtype} (user_id নেই, ফর্ম ভ্যালু ব্যবহার করা হচ্ছে)")

        # ৪. board_id -> board_name থাকলে board টেবিল থেকে পান
        board_name = data.get('board_name')
        print(f"🔍 ফর্ম থেকে board_name: '{board_name}'")
        print(f"🔍 ফর্ম থেকে board_id: '{data.get('board_id')}'")

        if board_name:
            table_board_id = self.get_board_id_from_board_table(board_name)
            final_board_id = table_board_id or data.get('board_id')
            print(f"🎯 চূড়ান্ত board_id: {final_board_id} (টেবিল: {table_board_id}, ফর্ম: {data.get('board_id')})")
        else:
            # ফর্ম থেকে board_id পেলে ক্রস-রেফারেন্স করুন
            form_board_id = data.get('board_id')
            if form_board_id:
                print(f"🔍 ফর্ম board_id দিয়ে board খোঁজা হচ্ছে: {form_board_id}")
                try:
                    board = Board.objects.filter(id=form_board_id).first()
                    if board:
                        print(f"✅ ID {form_board_id} দিয়ে board পাওয়া গেছে: '{board.board_name}'")
                        final_board_id = form_board_id
                    else:
                        print(f"⚠️ ID {form_board_id} দিয়ে কোনো board পাওয়া যায়নি")
                        final_board_id = form_board_id
                except Exception as e:
                    print(f"❌ ID দিয়ে board খুঁজতে সমস্যা: {e}")
                    final_board_id = form_board_id
            else:
                final_board_id = None
                print(f"🎯 কোনো board_id উপলব্ধ নেই")
            print(f"🎯 চূড়ান্ত board_id: {final_board_id}")

        # students_type নির্ধারণ
        board_id_for_logic = final_board_id
        irregular_year = data.get('irregular_year')

        print(f"📊 Board ডেটা:")
        print(f"  board_id: {board_id_for_logic}")
        print(f"  irregular_year: {irregular_year}")

        # লজিক: board_id 1 (মূল বেফাক) না হলে students_type = 'অনিয়মিত (অন্যান্য)' অন্যথায় 'নিয়মিত'
        if board_id_for_logic and board_id_for_logic != 1:
            students_type_val = 'অনিয়মিত (অন্যান্য)'
        else:
            students_type_val = 'নিয়মিত'

        # reg_no জেনারেট করুন (YY + 4 র্যান্ডম)
        year_last2 = str(timezone.now().year)[-2:]
        reg_no = int(f"{year_last2}{random.randint(1000,9999)}")

        try:
            # irregular_sub নিউমেরিক নিশ্চিত করুন
            try:
                irregular_sub_val = int(data.get('irregular_sub')) if data.get('irregular_sub') not in [None, ''] else 0
            except Exception:
                irregular_sub_val = 0

            basic = student_basic.objects.create(
                student_name_bn=data.get('student_name_bn',''),
                student_name_ar=data.get('student_name_ar',''),
                student_name_en=data.get('student_name_en',''),
                father_name_bn=data.get('father_name_bn',''),
                father_name_ar=data.get('father_name_ar',''),
                father_name_en=data.get('father_name_en',''),
                mother_name_bn=data.get('mother_name_bn',''),
                mother_name_ar=data.get('mother_name_ar',''),
                mother_name_en=data.get('mother_name_en',''),
                date_of_birth=data.get('date_of_birth'),
                roll_no=0,
                reg_no=reg_no,
                year=timezone.now().year,
                status='pending',
                students_type=students_type_val,
                exam_id=auto_exam_id,
                mobile=data.get('mobile',''),
                # বিশেষ লজিক ফিল্ড
                marhala_id=final_marhala_id,
                cid=final_cid,
                srtype=final_srtype,
                # স্বয়ংক্রিয়ভাবে ডিটেক্ট করা ফিল্ড
                madrasha_id=user_madrasha_id,
                markaz_id=auto_markaz_id,
                # নতুন ফিল্ড
                board_id=final_board_id,
                irregular_year=irregular_year or '',
                irregular_sub=irregular_sub_val,
                ip_address=request.META.get('REMOTE_ADDR','127.0.0.1'),
                created_at=timezone.now(),
                updated_at=timezone.now(),
                is_old=0,
            )
        except Exception as e:
            return Response({
                'error':'student_basic তৈরি করতে ব্যর্থ হয়েছে',
                'details':str(e)
            }, status=500)

        # ঠিকানা
        try:
            print(f"🏠 ঠিকানা ডেটা:")
            print(f"  division_id: {data.get('division_id','')}")
            print(f"  district_id: {data.get('district_id','')}")
            print(f"  thana_id: {data.get('thana_id','')}")
            
            student_adresss.objects.update_or_create(
                id=basic.id,
                defaults={
                    'student_id': basic.id,
                    'division': data.get('division_id',''),
                    'district': data.get('district_id',''),
                    'thana': data.get('thana_id',''),
                    'post_office': '',
                    'passport_photo': data.get('passport_photo',''),
                    'birth_certificate_no': data.get('birth_no',''),
                    'birth_certificate_photo': data.get('birth_attach',''),
                    'nid_no': data.get('nid_no',''),
                    'nid_photo': data.get('nid_attach',''),
                }
            )
            print(f"✅ ঠিকানা রেকর্ড তৈরি/আপডেট হয়েছে")
        except Exception as e:
            print(f"❌ ঠিকানা রেকর্ড তৈরিতে সমস্যা: {e}")
            pass

        # অ্যাটাচমেন্ট
        try:
            student_image_file = data.get('student_image')
            marksheet_file = data.get('marksheet')
            
            attachment_data = {
                'student_id': basic.id,
                'birth_no': data.get('birth_no',''),
                'birth_attach': data.get('birth_attach',''),
                'nid_no': data.get('nid_no',''),
                'nid_attach': data.get('nid_attach',''),
                'marksheet': marksheet_file.name if marksheet_file and hasattr(marksheet_file, 'name') else '',
            }
            
            student_attachment.objects.update_or_create(
                id=basic.id,
                defaults=attachment_data
            )
        except Exception as e:
            print(f"❌ অ্যাটাচমেন্ট তৈরিতে সমস্যা: {e}")
            pass

        return Response({
            'success': True,
            'message': 'ছাত্র সফলভাবে নিবন্ধিত হয়েছে',
            'student_id': basic.id,
            'reg_no': reg_no,
            'students_type': students_type_val,
            'board_id_saved': final_board_id,
            'irregular_year_saved': irregular_year,
            'madrasha_id': user_madrasha_id,
            'markaz_id': auto_markaz_id,
            'exam_id': auto_exam_id,
            'user_id_used': user_id,
            # ডিবাগিংয়ের জন্য বিশেষ লজিক ভ্যালু
            'marhala_id_saved': final_marhala_id,
            'cid_saved': final_cid,
            'srtype_saved': final_srtype,
            'header_marhala_id': header_marhala_id,
            'marhala_cid': marhala_cid,
            'header_srtype': header_srtype if user_id else None,
            'table_board_id': self.get_board_id_from_board_table(board_name) if board_name else None,
        }, status=201)