


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.model_homework import Homework
from ..permissions import IsTeacherOfStudentPermission
from ..serializers.homework_serializer import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HomeworkCreateAPIView(APIView):
    permission_classes = [IsTeacherOfStudentPermission,IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklash uchun
    """
    O'qituvchi yangi uy vazifasi yaratadi.
    """
    @swagger_auto_schema(responses={200:TopshirishSerializer(many=True)})
    def get(self,request):
        homework=Topshiriq.objects.all()
        serializer=TopshirishSerializer(homework,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



    @swagger_auto_schema(
        request_body=HomeWorkSerializer,  # Faqat request_body ishlatilmoqda
        operation_description="Yangi uy vazifasi yaratish. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},

        consumes = ["multipart/form-data"]  # Muhim!
    )

    def post(self, request):
        serializer = HomeWorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# STUDEN UYGA VAZIFANI TAYYORLAB YUKLAYDI

class HomeworkStudentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklash uchun
# UYGA VAZIFANI QOBIL QILIB OLADI
    @swagger_auto_schema(responses={200: HomeWorkSerializer(many=True)})
    def get(self, request):
        homework = Homework.objects.all()
        serializer = HomeWorkSerializer(homework, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=TopshirishSerializer,  # Faqat request_body ishlatilmoqda
        operation_description="Yangi uy vazifasi yuklandi. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},
        consumes = ["multipart/form-data"]  # Muhim!
    )
# UYGA VAZIFANI KORGANDAN SONG TAYYORLAB YUKLAYDI
    def post(self,request):
        serializer=TopshirishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# views/homework_views.py



class UyVazifasiniTekshirishAPIView(APIView):
    permission_classes = [IsTeacherOfStudentPermission,IsAuthenticated]

    """
    O'qituvchi talabalarning topshiriqlarini ko'rib chiqish
    """

    @swagger_auto_schema(
        operation_description="Bitta uy vazifasiga topshirilgan barcha topshiriqlarni ko'rish",
        manual_parameters=[
            openapi.Parameter(
                'homework_id',
                openapi.IN_PATH,
                description="Uy vazifasining ID raqami",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: TopshirishSerializer(many=True),
            404: "Uy vazifasi topilmadi"
        }
    )
    def get(self, request, homework_id):
        topshiriqlar = Topshiriq.objects.filter(homework_id=homework_id)
        if not topshiriqlar.exists():
            return Response({"xato": "Ushbu uy vazifasiga topshiriqlar topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TopshirishSerializer(topshiriqlar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Baholash(APIView):
    @swagger_auto_schema(
        operation_description="Talaba topshirig'ini baholash",
        manual_parameters=[
            openapi.Parameter(
                'topshiriq_id',
                openapi.IN_PATH,
                description="Baholanadigan topshiriqning ID raqami",
                type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=BaholashSerializer,
        responses={
            200: BaholashSerializer,
            400: "Noto'g'ri so'rov",
            404: "Topshiriq topilmadi"
        }
    )



    def patch(self, request, student_id):
        try:
            topshiriq = Topshiriq.objects.get(student_id=student_id)
        except Topshiriq.DoesNotExist:
            return Response({"xato": "Topshiriq topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BaholashSerializer(topshiriq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BahoniKorish(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(responses={200: BaholashSerializer()})
    def get(self,request,topshiriq_id):
        topshiriq = Topshiriq.objects.get(id=topshiriq_id)
        serializer=BaholashSerializer(topshiriq)
        return Response(serializer.data, status=status.HTTP_200_OK)




# qaysi studentni baholash

