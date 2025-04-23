


from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..add_pagination import CustomPagination
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
        student = Student.objects.all().order_by('-id')
        paginator = CustomPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(student, request)
        serializer = StudentSerializer(result_page, many=True)
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



