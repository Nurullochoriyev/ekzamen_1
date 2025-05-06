# Tashqi kutubxonalar va kerakli modullar import qilinmoqda
from drf_yasg import openapi  # Swagger uchun ochiq API hujjat parametrlari
from rest_framework import status, permissions  # DRFning status kodlari va ruxsat modullari
from app.permissions import IsTeacherOfStudentPermission  # Maxsus ruxsat sinfi (o'qituvchi - talaba aloqasi uchun)
from rest_framework.views import APIView  # DRFning asosiy APIView klasi
from ..serializers.attendance_serializers import *  # Davomat serializerlarini import qilish
from rest_framework.response import Response  # Javoblarni yuborish uchun DRF Response klasi
from drf_yasg.utils import swagger_auto_schema  # Swagger uchun avtomatik sxema generatori
from rest_framework.permissions import IsAuthenticated  # Foydalanuvchi avtorizatsiyadan o'tganligini tekshiradi

# ==== TALABA DAVOMATI API ====
# Talaba davomatlarini olish va yaratish uchun APIView
class AttendanceCreateAPIView(APIView):
    # Foydalanuvchi o'qituvchi va avtorizatsiyadan o'tgan bo'lishi kerak
    permission_classes = [IsTeacherOfStudentPermission, IsAuthenticated]

    # GET metodi orqali mavjud davomat yozuvlarini olish
    @swagger_auto_schema(responses={200: StudentAttendanceListSerializer(many=True)})  # Swagger uchun hujjat
    def get(self, request):
        attendance = StudentAttendance.objects.all()  # Barcha talaba davomatlarini olish
        serializers = StudentAttendanceListSerializer(attendance, many=True)  # Serializerga o'tkazish
        return Response(serializers.data, status=status.HTTP_200_OK)  # OK javobi bilan yuborish

    # POST metodi orqali yangi davomat yozuvi yaratish
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)  # Swagger uchun so'rov tanasi
    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)  # Kelgan malumotni serializerga joylash
        if serializer.is_valid():  # Malumot to'g'ri bo'lsa
            attendance = serializer.save()  # Saqlash
            return Response({  # Javob qaytarish
                'id': attendance.id,
                'group': attendance.group_id,
                'date': attendance.date,
                'descriptions': attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yaratildi'
            }, status=201)
        return Response(serializer.errors, status=400)  # Xatolik bo‘lsa, 400 qaytariladi

# Talaba davomatini PATCH qilish (qisman tahrirlash)
class AttendanceStudentPatch(APIView):
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)  # Swagger uchun
    def patch(self, request, attendance_id):
        try:
            attendance = Attendance.objects.get(id=attendance_id)  # ID bo'yicha modelni olish
        except Attendance.DoesNotExist:  # Agar topilmasa
            return Response(
                {'error': 'ID bo‘yicha maʼlumot topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Qisman yangilash uchun serializer
        serializer = AttendanceCreateSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_attendance = serializer.save()  # Saqlash
            return Response({
                'id': updated_attendance.id,
                'date': updated_attendance.date,
                'descriptions': updated_attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yangilandi'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik

# ==== O‘QITUVCHI DAVOMATI API ====
# Admin foydalanuvchilar uchun o'qituvchilar davomat API
class TeacherAttendanceAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Faqat adminlarga ruxsat

    # GET: O'qituvchilarning davomat ro'yxatini olish
    @swagger_auto_schema(responses={200: TeacherAttendanceSerializer(many=True)})
    def get(self, request):
        attendances = TeacherAttendance.objects.select_related(
            'teacher__user', 'attendance'
        ).order_by('-attendance__date')  # Eng so'nggi davomatlar bo‘yicha tartiblash

        serializer = TeacherAttendanceSerializer(attendances, many=True)  # Serializatsiya
        return Response(serializer.data, status=status.HTTP_200_OK)  # Javob

    # POST: Yangi o'qituvchi davomati yozuvini yaratish
    @swagger_auto_schema(request_body=TeacherAttendanceBulkSerializer)
    def post(self, request):
        serializer = TeacherAttendanceBulkSerializer(data=request.data)  # Ma'lumotni serializerga berish
        if serializer.is_valid(raise_exception=True):  # Validatsiya (xato bo'lsa avtomatik xato chiqaradi)
            attendance = serializer.save()  # Saqlash
            return Response({  # Muvaffaqiyatli javob
                'id': attendance.id,
                'date': attendance.date,
                'descriptions': attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yaratildi'
            }, status=201)
        return Response(serializer.errors, status=400)  # Xatolik

# PATCH: O'qituvchilar davomatini yangilash uchun API (admin uchun)
class TeacherAttendanceAPIViewPatch(APIView):
    permission_classes = [permissions.IsAdminUser]  # Faqat adminlarga ruxsat

    @swagger_auto_schema(
        request_body=TeacherAttendanceBulkSerializer,  # Yuboriladigan ma'lumot
        manual_parameters=[  # Swaggerda ko'rsatish uchun qo‘shimcha parametr
            openapi.Parameter(
                'attendance_id',
                openapi.IN_PATH,
                description="TAttendance ID raqami",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: TeacherAttendanceBulkSerializer,  # Muvaffaqiyatli yangilanish
            404: 'Davomat topilmadi',  # Topilmadi
            400: 'Noto\'g\'ri so\'rov'  # Xatolik
        }
    )
    def patch(self, request, attendance_id):
        try:
            attendance = TAttendance.objects.get(id=attendance_id)  # Modelni olish
        except TAttendance.DoesNotExist:
            return Response(
                {'error': 'Berilgan IDga mos davomat topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherAttendanceBulkSerializer(
            attendance,
            data=request.data,
            partial=True  # Qisman yangilash
        )

        if serializer.is_valid():
            updated_attendance = serializer.save()  # Saqlash
            return Response({  # Javob qaytarish
                'id': updated_attendance.id,
                'date': updated_attendance.date,
                'descriptions': updated_attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yangilandi'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik
