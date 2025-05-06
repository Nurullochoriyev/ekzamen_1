# Django va DRF importlari
from django.contrib.auth.hashers import make_password  # Parolni xashlash uchun
from django.db import transaction  # Bitta blok ichida bir nechta bazaviy amalni xavfsiz bajarish uchun
from django.shortcuts import get_object_or_404  # Ob'ektni olish, agar topilmasa 404 qaytaradi
from drf_yasg.utils import swagger_auto_schema  # Swagger uchun view metodlarini bezash
from rest_framework import status  # Javob status kodlari uchun
from rest_framework.permissions import IsAuthenticated  # Foydalanuvchi avtorizatsiyasini tekshirish
from rest_framework.views import APIView  # DRF bazaviy API view
from rest_framework.response import Response  # JSON javoblar uchun
from drf_yasg import openapi  # Swagger uchun parametrlar aniqlash

# Loyhadagi kerakli modullarni chaqirib olamiz
from ..permissions import *  # Custom permissionlar
from ..models import Student  # Student modelini chaqiramiz
from ..serializers.student_serializer import *  # Serializerni chaqiramiz
from ..add_pagination import CustomPagination  # Maxsus pagination class

# === STUDENTLAR UCHUN API CLASS ===
class StudentApi(APIView):
    # permission_classes = (IsAuthenticated,IsStaffUser,IsAdmin,IsAdminOrTeacherLimitedEdit)  # Faollashtirish mumkin

    # === STUDENTLARNI RO‘YXATINI OLISH (GET) ===
    @swagger_auto_schema(
        responses={200: StudentPostSerializer(many=True)},  # 200 statusda StudentPostSerializer listi qaytadi
        description="Studentlar ro'yxatini olish"  # Swaggerda chiqadigan izoh
    )
    def get(self, request):
        students = Student.objects.all().order_by('-id')  # Barcha studentlar, ID bo‘yicha teskari tartibda
        paginator = CustomPagination()  # Maxsus pagination obyekt
        paginator.page_size = 10  # Har bir sahifada 10 ta
        result_page = paginator.paginate_queryset(students, request)  # Studentlar sahifalab ajratiladi
        serializer = StudentPostSerializer(result_page, many=True)  # Sahifalangan queryset serialize qilinadi
        return paginator.get_paginated_response(serializer.data)  # Sahifalangan JSON response

    # === YANGI STUDENT YARATISH (POST) ===
    @swagger_auto_schema(
        request_body=StudentPostSerializer,  # Kiruvchi JSON uchun serializer
        description="Yangi student yaratish"  # Swaggerdagi tushuntirish
    )
    def post(self, request):
        data = request.data.copy()  # So‘rovdagi ma'lumotlardan nusxa olamiz
        group = data.get('group', '')  # group maydoni olish
        if isinstance(group, str):  # Agar string bo‘lsa (masalan: "1,2")
            data['group'] = list(map(int, group.split(',')))  # Listga aylantiramiz
        serializer = StudentPostSerializer(data=data)  # Serializerga ma'lumot beramiz
        if serializer.is_valid():  # Tekshiramiz
            student = serializer.save()  # Saqlaymiz
            return Response(data=StudentPostSerializer(student).data, status=status.HTTP_201_CREATED)  # Javob
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik bo‘lsa

    # === TO‘LIQ YANGILASH (PUT) ===
    @swagger_auto_schema(
        request_body=StudentPostSerializer,  # To‘liq yangilash uchun serializer
        manual_parameters=[  # Swaggerda query parametrlari ko‘rsatish
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,  # URL query (?id=1)
                description="O'zgartiriladigan student IDsi",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={  # Har xil statuslar uchun javoblar
            204: "Muvaffaqiyatli yangilandi",
            404: "Student topilmadi",
            500: "Server xatosi"
        },
        description="Studentni yangilash"
    )
    def put(self, request):
        data = request.data.copy()  # Kiruvchi ma'lumotdan nusxa
        group = data.get('group', '')  # Guruh maydoni
        if isinstance(group, str):  # String bo‘lsa listga aylantiramiz
            data['group'] = list(map(int, group.split(',')))

        student_id = request.query_params.get('id')  # URL querydan ID olamiz
        if not student_id:
            return Response({'detail': "ID ko'rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, pk=student_id)  # Student mavjudligini tekshiramiz
        serializer = StudentPostSerializer(student, data=data)  # Serializerga mavjud student va yangi data beriladi
        if serializer.is_valid():  # Ma'lumotlar to‘g‘ri bo‘lsa
            student = serializer.save()  # Saqlaymiz
            return Response(StudentPostSerializer(student).data, status=status.HTTP_200_OK)  # Yangi ma’lumotni qaytaramiz
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Agar valid emas

    # === QISMAN YANGILASH (PATCH) ===
    @swagger_auto_schema(
        request_body=StudentUpdateSerializer,  # Patch uchun serializer
        responses={  # Javob statuslari
            200: "Muvaffaqiyatli qisman yangilandi",
            400: "Noto‘g‘ri ma’lumot",
            404: "Student topilmadi",
            500: "Server xatosi"
        },
        description="Studentni qisman yangilash"
    )
    def patch(self, request):
        data = request.data.copy()  # Nusxa olish
        group = data.get('group', '')
        if isinstance(group, str):  # Stringdan listga o‘tkazamiz
            data['group'] = list(map(int, group.split(',')))

        student_id = data.get('id')  # JSONdan ID olish
        if not student_id:
            return Response({'detail': "ID ko‘rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_id = int(student_id)  # Intga o‘tkazamiz
        except ValueError:
            return Response({'detail': "ID noto‘g‘ri formatda."}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=student_id)  # Student mavjudligini tekshirish
        serializer = StudentUpdateSerializer(student, data=data, partial=True)  # Qisman yangilash uchun
        if serializer.is_valid():
            student = serializer.save()
            return Response(StudentPostSerializer(student).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # === O‘CHIRISH (DELETE) ===
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="O'chiriladigan student IDsi",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={  # Javoblar
            204: "Muvaffaqiyatli o'chirildi",
            404: "Student topilmadi",
            500: "Server xatosi"
        },
        description="Studentni o'chirish"
    )
    def delete(self, request):
        data = {"success": True}
        try:
            student_id = request.GET.get('id')  # URL querydan ID olish
            if not student_id:
                return Response(
                    data={"success": False, "xabar": "ID parametri talab qilinadi"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            student = get_object_or_404(Student, id=student_id)  # Student topiladi
            user = student.user  # Studentga bog‘langan foydalanuvchi

            with transaction.atomic():  # Bitta tranzaksiyada o‘chirish
                student.delete()  # Studentni o‘chirish
                user.delete()  # Foydalanuvchini ham o‘chirish

            return Response(
                data={"success": True, "xabar": "Student muvaffaqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Student.DoesNotExist:
            return Response(
                data={"success": False, "xabar": "Student topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                data={"success": False, "xabar": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







































#
# from django.contrib.auth.hashers import make_password
# from django.db import transaction
# from django.shortcuts import get_object_or_404
# from drf_yasg import openapi
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
#
# from ..add_pagination import CustomPagination
# from ..models import Student, User
# from ..serializers.student_serializer import StudentSerializer, StudentSerializerPost,StudentUserSerializer
#
#
# class StudentApi(APIView):
#
#     @swagger_auto_schema(
#         responses={
#             200: StudentSerializerPost(many=True),
#             400: "Noto'g'ri so'rov"
#         }
#     )
#     def get(self, request):
#         data = {"success": True}
#         student = Student.objects.all().order_by('-id')
#         paginator = CustomPagination()
#         paginator.page_size = 2
#         result_page = paginator.paginate_queryset(student, request)
#         serializer = StudentSerializer(result_page, many=True)
#         data["student"] = serializer.data
#         return Response(data=data)
#
#
#
#     @swagger_auto_schema(request_body=StudentSerializerPost)
#     def post(self, request):
#         data = {"success": True}
#         user_data = request.data['user']
#         student_data = request.data['student']
#
#         user_serializer = StudentUserSerializer(data=user_data)
#         user_serializer.is_valid(raise_exception=True)
#
#         validated_user = user_serializer.validated_data
#         validated_user['password'] = make_password(validated_user['password'])
#         validated_user['is_student'] = True
#         validated_user['is_active'] = True
#
#         user = User.objects.create(**validated_user)
#
#         student_serializer = StudentSerializer(data=student_data)
#         student_serializer.is_valid(raise_exception=True)
#
#         student = student_serializer.save(user=user)
#
#         if 'departments' in student_data:
#             student.departments.set(student_data['departments'])
#         if 'course' in student_data:
#             student.course.set(student_data['course'])
#
#         data['user'] = StudentUserSerializer(user).data
#         data['student'] = StudentSerializer(student).data
#         return Response(data)
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
#         javob = {"success": True}
#
#         try:
#             # ID ni so'rovdan olish
#             student_id = request.GET.get('id')
#             if not student_id:
#                 return Response(
#                     {"success": False, "xabar": "ID parametri talab qilinadi"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             # Studentni topish
#             student = get_object_or_404(Student, id=student_id)
#             user = student.user  # Bog'langan foydalanuvchi
#
#             # Transaction ichida o'chirish
#             with transaction.atomic():
#                 student.delete()  # Avval Student o'chiramiz
#                 user.delete()  # Keyin foydalanuvchini o'chiramiz
#
#             return Response(
#                 {"success": True, "xabar": "Student muvaffaqiyatli o'chirildi"},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#
#         except Student.DoesNotExist:
#             return Response(
#                 {"success": False, "xabar": "Student topilmadi"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as xato:
#             return Response(
#                 {"success": False, "xabar": str(xato)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#
#     def patch(self,request):
#         pass
#
#
#
