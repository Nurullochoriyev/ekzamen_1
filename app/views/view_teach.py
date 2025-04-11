from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherCreateSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Crud_Teacher(APIView):
    # @swagger_auto_schema(
    #     responses={
    #         200: TeacherSerializer(many=True),
    #         400: "Noto'g'ri so'rov"
    #     }
    # )
    # def get(self, request):
    #     teachers = Teacher.objects.all()
    #     serializer = TeacherSerializer(teachers, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # @swagger_auto_schema(request_body=TeacherSerializer)
    # def post(self,request):
    #     serializer=TeacherSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    #     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: TeacherSerializer(many=True),
            400: "Noto'g'ri so'rov"
        }
    )
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TeacherCreateSerializer,
        responses={
            201: TeacherSerializer,
            400: "Noto'g'ri ma'lumot"
        }
    )
    def post(self, request):
        serializer = TeacherCreateSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            response_serializer = TeacherSerializer(teacher)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=TeacherSerializer,
        responses={
            200: TeacherSerializer,
            404: "O'qituvchi topilmadi",
            400: "Noto'g'ri ma'lumot"
        }
    )
    def put(self, request):
        phone_number = request.data.get("phone_number")

        try:
            with transaction.atomic():
                # Teacher va User obyektlarini olamiz
                teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
                user = teacher.user

                # User ma'lumotlarini yangilaymiz
                user_data = {
                    'phone_number': request.data.get('phone_number', user.phone_number),
                    'full_name': request.data.get('full_name', user.full_name),
                    'is_active': request.data.get('is_active', user.is_active)
                }

                # Agar yangi parol kiritilgan bo'lsa
                if 'password' in request.data:
                    user.set_password(request.data['password'])

                # User ma'lumotlarini yangilaymiz
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()

                # Teacher ma'lumotlarini yangilaymiz
                serializer = TeacherSerializer(teacher, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                updated_teacher = serializer.save()

                # ManyToMany maydonlarini yangilaymiz
                if 'departments' in request.data:
                    updated_teacher.departments.set(request.data['departments'])
                if 'course' in request.data:
                    updated_teacher.course.set(request.data['course'])

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({"detail": "O'qituvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Telefon raqam')
            },
            required=['phone_number']
        ),
        responses={
            204: "O'qituvchi muvaffaqiyatli o'chirildi",
            404: "O'qituvchi topilmadi",
            400: "Noto'g'ri so'rov"
        }
    )





    def delete(self, request):
        phone_number = request.data.get("phone_number")

        try:
            with transaction.atomic():
                # Teacher va User obyektlarini olamiz
                teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
                user = teacher.user

                # Avval Teacher ni o'chiramiz (OneToOne munosabat)
                teacher.delete()

                # Keyin User ni o'chiramiz
                user.delete()

                return Response(
                    {"detail": "O'qituvchi va foydalanuvchi muvaffaqiyatli o'chirildi"},
                    status=status.HTTP_204_NO_CONTENT
                )

        except Teacher.DoesNotExist:
            return Response(
                {"detail": "O'qituvchi topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"O'chirishda xatolik: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )








    #
    # @swagger_auto_schema(request_body=TeacherSerializer)
    # def put(self, request):
    #     phone_number = request.data.get("phone_number")
    #
    #     try:
    #         teacher = Teacher.objects.get(user__phone_number=phone_number)
    #     except Teacher.DoesNotExist:
    #         return Response({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     serializer = TeacherSerializer(teacher, data=request.data)
    #
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # @swagger_auto_schema(request_body=TeacherSerializer)
    # def delete(self, request):
    #     phone_number = request.data.get("phone_number")
    #     try:
    #         teacher = Teacher.objects.get(user__phone_number=phone_number)
    #     except Teacher.DoesNotExist:
    #         return Response({"detail": "O'qituvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # Serializer o'chirish uchun kerak emas - bevosita obyektni o'chiramiz
    #     teacher.delete()
    #     return Response({"detail": "O'qituvchi muvaffaqiyatli o'chirildi"},
    #                     status=status.HTTP_204_NO_CONTENT)
    #
    #
    #
    #
