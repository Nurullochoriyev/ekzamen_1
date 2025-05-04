from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..permissions import IsStaffUser,IsTeacher,IsAdminOrTeacherLimitedEdit
from ..add_pagination import CustomPagination
from ..models.model_teacher import *
from ..serializers import  UserSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.teacher_serializers import TeacherPostSerializer, TeacherSerializer, TeacherUpdateSerializer

# TEACHER TOLIQ ISHLAYAPDI

class Teacher_Api(APIView):
    # permission_classes = [IsAuthenticated, IsStaffUser]
    #teacher ishlayapdi get
    @swagger_auto_schema(
        responses={200: TeacherPostSerializer(many=True)}
    )
    def get(self,request):
        data = {"success": True}
        teachers = Teacher.objects.all().order_by('-id')
        paginator = CustomPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(teachers, request)
        serializer =  TeacherPostSerializer(result_page, many=True)
        data["teacher"] = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)
# post ishlayapdi
    @swagger_auto_schema(
        request_body=TeacherPostSerializer
    )
    # TEACHERNI POST QILISH
    def post(self, request):
        data = request.data.copy()  # dict nusxasini olamiz

        # 'departments' ni string bo‘lsa, listga aylantirish
        departments = data.get('departments', '')
        if isinstance(departments, str):
            data['departments'] = list(map(int, departments.split(',')))

        # 'course' ni string bo‘lsa, listga aylantirish
        course = data.get('course', '')
        if isinstance(course, str):
            data['course'] = list(map(int, course.split(',')))

        serializer = TeacherPostSerializer(data=data)
        if serializer.is_valid():     #VALIDATSIYADAN O'TKIZADI
            serializer.save()          #AGAR O'TSA SAQLAYDI
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TeacherPostSerializer,
        manual_parameters=[

            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="O'zgartiriladigan  o'qituvchi IDsi",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Muvaffaqiyatli o'zgartirildi",
            404: "O'qituvchi topilmadi",
            500: "Server xatosi"
        }
    )
    def put(self, request):
        data = request.data.copy()  # So'rovni o'zgartirish uchun nusxa

        # 'departments' ni string bo'lsa, listga aylantiramiz
        departments = data.get('departments', '')
        if isinstance(departments, str):
            data['departments'] = list(map(int, departments.split(',')))

        # 'course' ni string bo'lsa, listga aylantiramiz
        course = data.get('course', '')
        if isinstance(course, str):
            data['course'] = list(map(int, course.split(',')))

        # IDni olish
        teacher_id = request.query_params.get('id')
        if not teacher_id:
            return Response({'detail': "ID ko'rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, pk=teacher_id)

        serializer = TeacherPostSerializer(teacher, data=data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # {
    #     "id": 3,
    #     "departments": [2, 3]   namuna patch
    # }
    # patch teacherni qisman malumotlarini o'zgartiradi
    #   muhum joyi (partial=True) techerni qisman malumoti kelyotgani bildiradi
    @swagger_auto_schema(
        request_body=TeacherUpdateSerializer,
        responses={
            200: "Muvaffaqiyatli qisman yangilandi",
            400: "Noto‘g‘ri ma’lumot",
            404: "O'qituvchi topilmadi",
            500: "Server xatosi"
        }
    )
    def patch(self, request):
        data = request.data.copy()

        # 'departments' ni string bo‘lsa listga aylantirish
        departments = data.get('departments', '')
        if isinstance(departments, str):
            data['departments'] = list(map(int, departments.split(',')))

        # 'course' ni string bo‘lsa listga aylantirish
        course = data.get('course', '')
        if isinstance(course, str):
            data['course'] = list(map(int, course.split(',')))

        # IDni olish va tekshirish
        teacher_id = data.get('id')
        if not teacher_id:
            return Response({'detail': "ID ko‘rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher_id = int(teacher_id)
        except ValueError:
            return Response({'detail': "ID noto‘g‘ri formatda."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, id=teacher_id)

        # Qisman yangilash
        serializer = TeacherUpdateSerializer(teacher, data=data, partial=True)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete ishlayapdi
    # teacherni o'chirish bunda user ham birgalikda o'chadi
    # удалит учителя с пользователем
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="O'chiriladigan o'qituvchi IDsi",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Muvaffaqiyatli o'chirildi",
            404: "O'qituvchi topilmadi",
            500: "Server xatosi"
        }
    )
    def delete(self, request):
        data = {"success": True}

        try:
            # ID ni so'rovdan olish
            teacher_id = request.GET.get('id')
            if not teacher_id:
                return Response(
                    data={"success": False, "xabar": "ID parametri talab qilinadi"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # O'qituvchini topish
            teacher = get_object_or_404(Teacher, id=teacher_id)
            user = teacher.user  # Bog'langan foydalanuvchi

            # Transaction ichida o'chirish
            with transaction.atomic():
                teacher.delete()  # Avval o'qituvchini o'chiramiz
                user.delete()  # Keyin foydalanuvchini o'chiramiz

            return Response(
                data={"success": True, "xabar": "O'qituvchi muvaffaqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Teacher.DoesNotExist:
            return Response(
                data={"success": False, "xabar": "O'qituvchi topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as xato:
            return Response(
                data={"success": False, "xabar": str(xato)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




















#
# class TeacherApi(APIView):
#     @swagger_auto_schema(
#         responses={
#             200: TeacherSerializerPost(many=True),
#             400: "Noto'g'ri so'rov"
#         }
#     )
#     def get(self, request):
#         data = {"success": True}
#         teacher = Teacher.objects.all().order_by('-id')
#         paginator=CustomPagination()
#         paginator.page_size=2
#         result_page=paginator.paginate_queryset(teacher,request)
#         serializer = TeacherSerializer(result_page, many=True)
#         data["teacher"] = serializer.data
#         return Response(data=data)
#
#
#           TOGRI VARYANT (ISHLAYDI POST)
#     @swagger_auto_schema(request_body=TeacherSerializerPost)
#     def post(self, request):
#         # Boshlang'ich javob ma'lumoti
#         javob = {"success": True}  # "muvaffaqiyatli": True deb ham yozish mumkin
#
#         try:
#             # 1. So'rovdan ma'lumotlarni olish
#             foydalanuvchi_maqlumotlari = request.data["user"]
#             oqituvchi_maqlumotlari = request.data["teacher"]
#             telefon_raqami = foydalanuvchi_maqlumotlari["phone_number"]
#
#             # 2. Foydalanuvchini yaratish va tekshirish
#             foydalanuvchi_serializer = UserSerializer(data=foydalanuvchi_maqlumotlari)
#             if not foydalanuvchi_serializer.is_valid():
#                 return Response(
#                     data={"success": False, "xatolar": foydalanuvchi_serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST  # Noto'g'ri so'rov kodi
#                 )
#
#             # Parolni shifrlash va qo'shimcha maydonlarni to'ldirish
#             tasdiqlangan_maqlumot = foydalanuvchi_serializer.validated_data
#             tasdiqlangan_maqlumot['password'] = make_password(tasdiqlangan_maqlumot.get("password"))
#             tasdiqlangan_maqlumot['is_teacher'] = True  # Bu o'qituvchi ekanligi
#             tasdiqlangan_maqlumot['is_active'] = True  # Faol foydalanuvchi
#
#             # Foydalanuvchini saqlash
#             yangi_foydalanuvchi = foydalanuvchi_serializer.save()
#
#             # 3. O'qituvchi ma'lumotlarini tayyorlash
#             oqituvchi_maqlumotlari["user"] = yangi_foydalanuvchi.id
#             oqituvchi_serializer = TeacherSerializer(data=oqituvchi_maqlumotlari)
#
#             if not oqituvchi_serializer.is_valid():
#                 # Agar o'qituvchi yaratilmagan bo'lsa, foydalanuvchini o'chiramiz
#                 yangi_foydalanuvchi.delete()
#                 return Response(
#                     data={"success": False, "xatolar": oqituvchi_serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             # O'qituvchini saqlash
#             oqituvchi_serializer.save()
#
#             # 4. Muvaffaqiyatli javob qaytarish
#             javob['data'] = foydalanuvchi_serializer.data
#             return Response(data=javob, status=status.HTTP_201_CREATED)  # Yaratildi kodi
#
#         # Xatoliklarni qo'llash
#         except KeyError as xato:
#             return Response(
#                 data={"success": False, "xabar": f"So'rovda yetishmayotgan kalit: {str(xato)}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as xato:
#             return Response(
#                 data={"success": False, "xabar": str(xato)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR  # Server xatosi kodi
#             )
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'id',
#                 openapi.IN_QUERY,
#                 description="O'chiriladigan o'qituvchi IDsi",
#                 type=openapi.TYPE_INTEGER,
#                 required=True
#             )
#         ],
#         responses={
#             204: "Muvaffaqiyatli o'chirildi",
#             404: "O'qituvchi topilmadi",
#             500: "Server xatosi"
#         }
#     )
#     def delete(self, request):
#         data = {"success": True}
#
#         try:
#             # ID ni so'rovdan olish
#             teacher_id = request.GET.get('id')
#             if not teacher_id:
#                 return Response(
#                     data={"success": False, "xabar": "ID parametri talab qilinadi"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             # O'qituvchini topish
#             teacher = get_object_or_404(Teacher, id=teacher_id)
#             user = teacher.user  # Bog'langan foydalanuvchi
#
#             # Transaction ichida o'chirish
#             with transaction.atomic():
#                 teacher.delete()  # Avval o'qituvchini o'chiramiz
#                 user.delete()  # Keyin foydalanuvchini o'chiramiz
#
#             return Response(
#                 data={"success": True, "xabar": "O'qituvchi muvaffaqiyatli o'chirildi"},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#
#         except Teacher.DoesNotExist:
#             return Response(
#                 data={"success": False, "xabar": "O'qituvchi topilmadi"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as xato:
#             return Response(
#                 data={"success": False, "xabar": str(xato)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#
#     def put(self, request, pk):
#         teacher = get_object_or_404(Teacher, pk=pk)
#         serializer = TeacherSerializerPost(teacher, data=request.data)
#
#         if serializer.is_valid():
#             teacher = serializer.save()
#             return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         teacher = get_object_or_404(Teacher, pk=pk)
#         serializer = TeacherSerializerPost(teacher, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             teacher = serializer.save()
#             return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
#
#
#
#
#
#
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from ..models import GroupStudent
# from ..permissions import *
# from ..serializers.group_serializer import GroupNameSerializer
#
# class GroupNameUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = GroupNameSerializer
#     permission_classes = [permissions.IsAuthenticated, IsTeacher]
#
#     def get_queryset(self):
#         # Faqat o'zining guruhlarini ko'rish
#         return GroupStudent.objects.filter(teacher=self.request.user)
#
#     def patch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#
#         # Faqat name fieldini yangilashga ruxsat beramiz
#         instance.name = serializer.validated_data.get('name', instance.name)
#         instance.save()
#
#         return Response(serializer.data)
#
#
#
#
#
#
#
#
#
#
#
#
#















    #
    # @swagger_auto_schema(
    #     operation_description="ID orqali o'qituvchi ma'lumotlarini yangilash",
    #     request_body=TeacherUpdateSerializer,
    #     responses={
    #         200: TeacherUpdateSerializer,
    #         400: "Noto'g'ri so'rov formati",
    #         404: "O'qituvchi topilmadi"
    #     }
    # )
    # def patch(self, request, id):
    #     try:
    #         teacher = Teacher.objects.get(id=id)
    #         serializer = TeacherUpdateSerializer(teacher, data=request.data, partial=True)
    #
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({
    #                 'success': True,
    #                 'data': serializer.data
    #             })
    #
    #         return Response({
    #             'success': False,
    #             'errors': serializer.errors
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except Teacher.DoesNotExist:
    #         return Response({
    #             'success': False,
    #             'message': "O'qituvchi topilmadi"
    #         }, status=status.HTTP_404_NOT_FOUND)
    #
    #
    #
    #
    #
    #
    #


















    # @swagger_auto_schema(request_body=TeacherSerializerPost)
    # def post(self, request):
    #     data = {"success": True}
    #     user = request.data["user"]
    #     teacher = request.data["teacher"]
    #     phone_number = user["phone_number"]
    #     user_serializer = UserSerializer(data=user)
    #     if user_serializer.is_valid(raise_exception=True):
    #         user_serializer.is_teacher = True
    #         user_serializer.is_active = True
    #         user_serializer.password = (make_password(user_serializer.validated_data.get("password")))
    #         user_serializer.save()
    #         teacher_serializer = TeacherSerializer(data=teacher)
    #         user_id = User.objects.filter(phone_number=phone_number).values('id')[0]['id']
    #         teacher["user"] = user_id
    #         teacher_serializer = TeacherSerializer(data=teacher)
    #         if teacher_serializer.is_valid(raise_exception=True):
    #             teacher_serializer.save()
    #             data['data'] = user_serializer.data
    #             return Response(data=data)
    #         return Response(data=teacher_serializer.errors)
    #     return Response(data=user_serializer.errors)
















# class Crud_Teacher(APIView):
#     # @swagger_auto_schema(
#     #     responses={
#     #         200: TeacherSerializer(many=True),
#     #         400: "Noto'g'ri so'rov"
#     #     }
#     # )
#     # def get(self, request):
#     #     teachers = Teacher.objects.all()
#     #     serializer = TeacherSerializer(teachers, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     # @swagger_auto_schema(request_body=TeacherSerializer)
#     # def post(self,request):
#     #     serializer=TeacherSerializer(data=request.data)
#     #     if serializer.is_valid(raise_exception=True):
#     #         serializer.save()
#     #         return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#     #     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         responses={
#             200: TeacherSerializer(many=True),
#             400: "Noto'g'ri so'rov"
#         }
#     )
#     def get(self, request):
#         teachers = Teacher.objects.all()
#         serializer = TeacherSerializer(teachers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         request_body=TeacherCreateSerializer,
#         responses={
#             201: TeacherSerializer,
#             400: "Noto'g'ri ma'lumot"
#         }
#     )
#     def post(self, request):
#         serializer = TeacherCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             teacher = serializer.save()
#             response_serializer = TeacherSerializer(teacher)
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         request_body=TeacherSerializer,
#         responses={
#             200: TeacherSerializer,
#             404: "O'qituvchi topilmadi",
#             400: "Noto'g'ri ma'lumot"
#         }
#     )
#     def put(self, request):
#         phone_number = request.data.get("phone_number")
#
#         try:
#             with transaction.atomic():
#                 # Teacher va User obyektlarini olamiz
#                 teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
#                 user = teacher.user
#
#                 # User ma'lumotlarini yangilaymiz
#                 user_data = {
#                     'phone_number': request.data.get('phone_number', user.phone_number),
#                     'full_name': request.data.get('full_name', user.full_name),
#                     'is_active': request.data.get('is_active', user.is_active)
#                 }
#
#                 # Agar yangi parol kiritilgan bo'lsa
#                 if 'password' in request.data:
#                     user.set_password(request.data['password'])
#
#                 # User ma'lumotlarini yangilaymiz
#                 for attr, value in user_data.items():
#                     setattr(user, attr, value)
#                 user.save()
#
#                 # Teacher ma'lumotlarini yangilaymiz
#                 serializer = TeacherSerializer(teacher, data=request.data, partial=True)
#                 serializer.is_valid(raise_exception=True)
#                 updated_teacher = serializer.save()
#
#                 # ManyToMany maydonlarini yangilaymiz
#                 if 'departments' in request.data:
#                     updated_teacher.departments.set(request.data['departments'])
#                 if 'course' in request.data:
#                     updated_teacher.course.set(request.data['course'])
#
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#
#         except Teacher.DoesNotExist:
#             return Response({"detail": "O'qituvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Telefon raqam')
#             },
#             required=['phone_number']
#         ),
#         responses={
#             204: "O'qituvchi muvaffaqiyatli o'chirildi",
#             404: "O'qituvchi topilmadi",
#             400: "Noto'g'ri so'rov"
#         }
#     )
#
#
#
#
#
#     def delete(self, request):
#         phone_number = request.data.get("phone_number")
#
#         try:
#             with transaction.atomic():
#                 # Teacher va User obyektlarini olamiz
#                 teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
#                 user = teacher.user
#
#                 # Avval Teacher ni o'chiramiz (OneToOne munosabat)
#                 teacher.delete()
#
#                 # Keyin User ni o'chiramiz
#                 user.delete()
#
#                 return Response(
#                     {"detail": "O'qituvchi va foydalanuvchi muvaffaqiyatli o'chirildi"},
#                     status=status.HTTP_204_NO_CONTENT
#                 )
#
#         except Teacher.DoesNotExist:
#             return Response(
#                 {"detail": "O'qituvchi topilmadi"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {"detail": f"O'chirishda xatolik: {str(e)}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#
#
#
#
#
#
#
#     #
#     # @swagger_auto_schema(request_body=TeacherSerializer)
#     # def put(self, request):
#     #     phone_number = request.data.get("phone_number")
#     #
#     #     try:
#     #         teacher = Teacher.objects.get(user__phone_number=phone_number)
#     #     except Teacher.DoesNotExist:
#     #         return Response({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     serializer = TeacherSerializer(teacher, data=request.data)
#     #
#     #     if serializer.is_valid(raise_exception=True):
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # @swagger_auto_schema(request_body=TeacherSerializer)
#     # def delete(self, request):
#     #     phone_number = request.data.get("phone_number")
#     #     try:
#     #         teacher = Teacher.objects.get(user__phone_number=phone_number)
#     #     except Teacher.DoesNotExist:
#     #         return Response({"detail": "O'qituvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     # Serializer o'chirish uchun kerak emas - bevosita obyektni o'chiramiz
#     #     teacher.delete()
#     #     return Response({"detail": "O'qituvchi muvaffaqiyatli o'chirildi"},
#     #                     status=status.HTTP_204_NO_CONTENT)
#     #
#     #
#     #
#     #
