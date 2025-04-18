# from django.contrib.auth.hashers import make_password
# from django.db import transaction
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
# from rest_framework.views import APIView
#
# from ..models import Student
# from ..models.model_teacher import *
# from ..serializers import StudentSerializer, UserSerializer
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from ..serializers.student_serializer import StudentSerializerPost, ParentsSerializer
# #
# #
# class StudentApi(APIView):
#     @swagger_auto_schema(
#         responses={
#             200: StudentSerializerPost(many=True),
#             400: "Noto'g'ri so'rov"
#         }
#     )
#     def get(self, request):
#         data = {"success": True}
#         students = Student.objects.all()
#         serializer = StudentSerializer(students, many=True)
#         data["students"] = serializer.data
#         return Response(data=data)
#
#     @swagger_auto_schema(request_body=StudentSerializerPost)
#     def post(self, request):
#         javob = {"success": True}
#
#         try:
#             # Transaction boshlaymiz - agar xato bo'lsa, barcha o'zgarishlar bekor qilinadi
#             with transaction.atomic():
#                 # 1. User ma'lumotlarini olish
#                 user_data = request.data["user"]
#                 student_data = request.data["student"]
#                 phone_number = user_data["phone_number"]
#
#                 # 2. User yaratish
#                 user_serializer = UserSerializer(data=user_data)
#                 if not user_serializer.is_valid():
#                     return Response(
#                         {"success": False, "errors": user_serializer.errors},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#
#                 # Parolni hash qilish va qo'shimcha maydonlar
#                 validated_user = user_serializer.validated_data
#                 validated_user['password'] = make_password(validated_user.get("password"))
#                 validated_user['is_student'] = True
#                 validated_user['is_active'] = True
#
#                 new_user = user_serializer.save()
#
#                 # 3. Student yaratish
#                 student_data["user"] = new_user.id
#                 student_serializer = StudentSerializer(data=student_data)
#
#                 if not student_serializer.is_valid():
#                     return Response(
#                         {"success": False, "errors": student_serializer.errors},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#
#                 student_serializer.save()
#
#                 # 4. Agar Parents ma'lumotlari kelsa, ularni ham yaratish
#                 if "parents" in request.data:
#                     parents_data = request.data["parents"]
#                     parents_data["student"] = student_serializer.instance.id
#                     parents_serializer = ParentsSerializer(data=parents_data)
#
#                     if not parents_serializer.is_valid():
#                         return Response(
#                             {"success": False, "errors": parents_serializer.errors},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#
#                     parents_serializer.save()
#
#                 javob['data'] = {
#                     'user': user_serializer.data,
#                     'student': student_serializer.data
#                 }
#                 if "parents" in request.data:
#                     javob['data']['parents'] = parents_serializer.data
#
#                 return Response(javob, status=status.HTTP_201_CREATED)
#
#         except KeyError as e:
#             return Response(
#                 {"success": False, "message": f"Missing key in request: {str(e)}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {"success": False, "message": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#
#


from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..models import Student, User
from ..serializers.student_serializer import StudentSerializer, StudentSerializerPost,StudentUserSerializer


class StudentApi(APIView):

    @swagger_auto_schema(
        responses={
            200: StudentSerializerPost(many=True),
            400: "Noto'g'ri so'rov"
        }
    )
    def get(self, request):
        data = {"success": True}
        teacher = Student.objects.all()
        serializer = StudentSerializer(teacher, many=True)
        data["teacher"] = serializer.data
        return Response(data=data)



    @swagger_auto_schema(request_body=StudentSerializerPost)
    def post(self, request):
        data = {"success": True}
        user_data = request.data['user']
        student_data = request.data['student']

        user_serializer = StudentUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        validated_user = user_serializer.validated_data
        validated_user['password'] = make_password(validated_user['password'])
        validated_user['is_student'] = True
        validated_user['is_active'] = True

        user = User.objects.create(**validated_user)

        student_serializer = StudentSerializer(data=student_data)
        student_serializer.is_valid(raise_exception=True)

        student = student_serializer.save(user=user)

        if 'departments' in student_data:
            student.departments.set(student_data['departments'])
        if 'course' in student_data:
            student.course.set(student_data['course'])

        data['user'] = StudentUserSerializer(user).data
        data['student'] = StudentSerializer(student).data
        return Response(data)

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
        javob = {"success": True}

        try:
            # ID ni so'rovdan olish
            student_id = request.GET.get('id')
            if not student_id:
                return Response(
                    {"success": False, "xabar": "ID parametri talab qilinadi"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Studentni topish
            student = get_object_or_404(Student, id=student_id)
            user = student.user  # Bog'langan foydalanuvchi

            # Transaction ichida o'chirish
            with transaction.atomic():
                student.delete()  # Avval Student o'chiramiz
                user.delete()  # Keyin foydalanuvchini o'chiramiz

            return Response(
                {"success": True, "xabar": "Student muvaffaqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Student.DoesNotExist:
            return Response(
                {"success": False, "xabar": "Student topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as xato:
            return Response(
                {"success": False, "xabar": str(xato)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self,request):
        pass