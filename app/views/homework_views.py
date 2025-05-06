# DRF parserlari fayl yuklash uchun
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated  # Foydalanuvchi avtorizatsiyadan o'tganligini tekshiradi
from rest_framework.views import APIView  # DRFning asosiy View klassi
from rest_framework.response import Response  # Javob obyektini shakllantiradi
from rest_framework import status  # HTTP status kodlar

# Model, permission va serializerlar import qilinmoqda
from ..models.model_homework import Homework  # Homework modeli
from ..permissions import IsTeacherOfStudentPermission  # O'qituvchining talaba bilan bog‘liqligini tekshiruvchi permission
from ..serializers.homework_serializer import *  # Homeworkga oid serializerlar

from drf_yasg.utils import swagger_auto_schema  # Swagger hujjatlash uchun
from drf_yasg import openapi  # Swagger parametrlari

# === O'qituvchi uyga vazifa yuklaydi, talaba yuklaydi, o'qituvchi tekshiradi ===

# Uyga vazifa yaratish (O'qituvchi uchun)
class HomeworkCreateAPIView(APIView):
    permission_classes = [IsTeacherOfStudentPermission, IsAuthenticated]  # Ruxsat: o'qituvchi va login bo‘lgan foydalanuvchi

    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklashga ruxsat beruvchi parserlar

    """
    O'qituvchi yangi uy vazifasi yaratadi.
    """

    @swagger_auto_schema(responses={200: TopshirishSerializer(many=True)})  # Swagger javob sxemasi
    def get(self, request):
        homework = Topshiriq.objects.all()  # Barcha topshiriqlarni olish
        serializer = TopshirishSerializer(homework, many=True)  # Serializatsiya qilish
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 OK javob

    @swagger_auto_schema(
        request_body=HomeWorkSerializer,  # Yuborilayotgan ma'lumot
        operation_description="Yangi uy vazifasi yaratish. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},
        consumes=["multipart/form-data"]  # Fayl yuklash formatini bildiradi
    )
    def post(self, request):
        serializer = HomeWorkSerializer(data=request.data)  # Serializerga ma’lumot berish
        if serializer.is_valid():
            serializer.save()  # Saqlash
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Muvaffaqiyatli javob
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xato bo‘lsa

# === Talaba uyga vazifani ko‘radi va yuklaydi ===
class HomeworkStudentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklash uchun

    # Vazifalarni ko‘rish
    @swagger_auto_schema(responses={200: HomeWorkSerializer(many=True)})
    def get(self, request):
        homework = Homework.objects.all()  # Barcha uy vazifalari
        serializer = HomeWorkSerializer(homework, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TopshirishSerializer,
        operation_description="Talaba uy vazifasini yuklaydi. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},
        consumes=["multipart/form-data"]
    )
    def post(self, request):
        serializer = TopshirishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Xato bo‘lsa avtomatik chiqaradi
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# === O'qituvchi uy vazifasini tekshiradi ===
class UyVazifasiniTekshirishAPIView(APIView):
    permission_classes = [IsTeacherOfStudentPermission, IsAuthenticated]  # Ruxsat kerak

    """
    O'qituvchi talabalarning topshiriqlarini ko‘rib chiqadi
    """

    @swagger_auto_schema(
        operation_description="Bitta uy vazifasiga topshirilgan barcha topshiriqlarni ko‘rish",
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
        topshiriqlar = Topshiriq.objects.filter(homework_id=homework_id)  # Homework ID bo‘yicha topshiriqlar
        if not topshiriqlar.exists():
            return Response({"xato": "Ushbu uy vazifasiga topshiriqlar topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TopshirishSerializer(topshiriqlar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# === O'qituvchi baho qo‘yadi (PATCH) ===
class Baholash(APIView):
    @swagger_auto_schema(
        operation_description="Talabaning topshirig‘ini baholash",
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
    def patch(self, request, student_id):  # E'tibor bering: parametr nomi topshiriq_id emas, student_id
        try:
            topshiriq = Topshiriq.objects.get(student_id=student_id)  # Student ID bo‘yicha topshiriqni olish
        except Topshiriq.DoesNotExist:
            return Response({"xato": "Topshiriq topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BaholashSerializer(topshiriq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# === Talaba o‘z bahosini ko‘radi ===
class BahoniKorish(APIView):
    permission_classes = (IsAuthenticated,)  # Foydalanuvchi login bo‘lgan bo‘lishi kerak

    @swagger_auto_schema(responses={200: BaholashSerializer()})
    def get(self, request, topshiriq_id):
        topshiriq = Topshiriq.objects.get(id=topshiriq_id)  # Topshiriqni ID bo‘yicha olish
        serializer = BaholashSerializer(topshiriq)
        return Response(serializer.data, status=status.HTTP_200_OK)
